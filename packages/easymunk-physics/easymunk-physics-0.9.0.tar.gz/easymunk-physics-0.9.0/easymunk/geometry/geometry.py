"""
Geometric utility functions.
"""
from functools import partial
from itertools import chain
from math import sqrt
from typing import Sequence, Tuple, cast, List

import sidekick.api as sk

from ..cp import lib
from ..linalg.math import sign
from ..linalg import Vec2d
from ..typing import VecLike


def moment_for_circle(
    mass: float,
    inner_radius: float,
    outer_radius: float,
    offset: VecLike = (0, 0),
) -> float:
    """Calculate the moment of inertia for a hollow circle

    (A solid circle has an inner radius of 0)
    """
    assert len(offset) == 2

    return lib.cpMomentForCircle(mass, inner_radius, outer_radius, offset)


def moment_for_segment(mass: float, a: VecLike, b: VecLike, radius: float) -> float:
    """Calculate the moment of inertia for a line segment

    The endpoints a and b are relative to the body
    """
    return lib.cpMomentForSegment(mass, a, b, radius)


def moment_for_box(mass: float, size: VecLike) -> float:
    """Calculate the moment of inertia for a solid box centered on the body.

    size should be a tuple of (width, height)
    """
    return lib.cpMomentForBox(mass, size[0], size[1])


def moment_for_poly(
    mass: float,
    vertices: Sequence[VecLike],
    offset: VecLike = (0, 0),
    radius: float = 0,
) -> float:
    """Calculate the moment of inertia for a solid polygon shape.

    Assumes the polygon center of gravity is at its centroid. The offset is
    added to each vertex.
    """
    vs = list(vertices)
    return lib.cpMomentForPoly(mass, len(vs), vs, offset, radius)


def area_for_circle(inner_radius: float, outer_radius: float) -> float:
    """Area of a hollow circle."""
    return cast(float, lib.cpAreaForCircle(inner_radius, outer_radius))


def area_for_segment(a: VecLike, b: VecLike, radius: float) -> float:
    """Area of a beveled segment.

    (Will always be zero if radius is zero)
    """
    return lib.cpAreaForSegment(a, b, radius)


def area_for_poly(vertices: Sequence[VecLike], radius: float = 0) -> float:
    """
    Signed area of a polygon shape.

    Returns a negative number for polygons with a clockwise winding.
    """
    vs = list(vertices)
    return lib.cpAreaForPoly(len(vs), vs, radius)


def is_clockwise(points):
    """
    Return True if the points given form a clockwise polygon.
    """
    a = 0
    for i in range(len(points)):
        j = i + 1
        if j == len(points):
            j = 0
        a += points[i][0] * points[j][1] - points[i][1] * points[j][0]
    return a <= 0  # or is it the other way around?


def is_left(p0, p1, p2) -> int:
    """Test if p2 is left, on or right of the (infinite) line (p0,p1).

    :return: > 0 for p2 left of the line through p0 and p1
        = 0 for p2 on the line
        < 0 for p2 right of the line
    """
    # cast the answer to an int so it can be used directly from sort()
    # cast is not a good idea.. use something else
    # return int((p1.x - p0.x)*(p2.y-p0.y) - (p2.x-p0.x)*(p1.y-p0.y))
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    sorting = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    if sorting > 0:
        return 1
    elif sorting < 0:
        return -1
    else:
        return 0


def is_convex(points: Sequence[Vec2d]) -> bool:
    """Test if a polygon (list of (x,y)) is convex or not

    :return: True if the polygon is convex, False otherwise
    """
    if len(points) <= 2:
        raise ValueError("need at least 3 points to form a polygon")

    p0 = points[0]
    p1 = points[1]
    p2 = points[2]
    xc, yc = 0, 0
    is_same_winding = is_left(p0, p1, p2)
    for p2 in [*points[2:], p0, p1]:
        if is_same_winding != is_left(p0, p1, p2):
            return False
        a = p1 - p0
        b = p2 - p1  # p2-p1
        if sign(a.x) != sign(b.x):
            xc += 1
        if sign(a.y) != sign(b.y):
            yc += 1
        p0, p1 = p1, p2

    return xc <= 2 and yc <= 2


def reduce_poly(points, tolerance=0.5):
    """Remove close points to simplify a polyline
    tolerance is the min distance between two points squared.

    :return: The reduced polygon as a list of (x,y)
    """

    if len(points) == 0:
        return []

    x, y = points[0]
    reduced_ps = [Vec2d(x, y)]

    for u, v in points[1:]:
        distance = (x - u) ** 2 + (y - v) ** 2
        if distance > tolerance:
            x, y = u, v
            reduced_ps.append(Vec2d(u, v))

    return reduced_ps


def convex_hull(points):
    """Create a convex hull from a list of points.
    This function uses the Graham Scan Algorithm.

    :return: Convex hull as a list of (x,y)
    """

    if len(points) <= 2:
        raise ValueError("need at least 3 points to form a convex hull")

    # Find lowest rightmost point
    x, y = points[0]
    for u, v in points[1:]:
        if v < y:
            x, y = u, v
        elif v == y and u > x:
            x, y = u, v
    points.remove((x, y))

    # Sort the points angularly about p0 as center
    f = partial(is_left, (x, y))
    points.sort(key=_cmp_to_key(f))
    points.reverse()
    points.insert(0, (x, y))

    # Find the hull points
    hull = [(x, y), points[1]]

    for p in points[2:]:
        pt1 = hull[-1]
        pt2 = hull[-2]
        n = is_left(pt2, pt1, p)
        if n > 0:
            hull.append(p)
        else:
            while n <= 0 and len(hull) > 2:
                hull.pop()
                pt1 = hull[-1]
                pt2 = hull[-2]
                n = is_left(pt2, pt1, p)
            hull.append(p)
    return hull


def centroid(points: Sequence[VecLike], is_closed=False) -> Vec2d:
    """
    Calculate the centroid of a polygon.

    See Also:
        - http://en.wikipedia.org/wiki/Polygon
    """

    area = cx = cy = 0
    pts = iter(points if is_closed else chain(points, [points[0]]))
    (x, y) = next(pts)

    for (u, v) in pts:
        area += x * v - y * u
        cx += (x + u) * (x * v - y * u)
        cy += (y + v) * (x * v - y * u)
        (x, y) = (u, v)

    if area == 0:
        raise ValueError("polygon has a null area")
    area /= 2
    cx /= 6 * area
    cy /= 6 * area
    return Vec2d(cx, cy)


def poly_vectors_around_center(pointlist):
    """
    Rearranges vectors around the center

    :return: pointlist ([Vec2d/pos, ...])
    """

    cm = centroid(pointlist)
    return [pt - cm for pt in pointlist]


def calc_area(points: Sequence[VecLike]) -> float:
    """
    Calculate the area of a polygon
    """
    # ref: http://en.wikipedia.org/wiki/Polygon

    if len(points) < 3:
        return 0

    (x, y), rest = sk.uncons(points)
    area = 0
    for (u, v) in rest:
        area += x * v - u * y
        x, y = u, v

    return area * 0.5


def calc_perimeter(points):
    """Calculate the perimeter of a polygon

    :return: Perimeter of polygon
    """

    if len(points) < 2:
        return 0

    x, y = points[0]
    c = 0
    for u, v in points[1:] + [points[0]]:
        c += sqrt((u - x) ** 2 + (v - y) ** 2)
        x, y = u, v
    return c


def _cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function, useful for python 3"""

    class K(object):
        def __init__(self, obj, *_args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def _is_corner(a, b, c):
    # returns if point b is an outer corner
    return not (is_clockwise([a, b, c]))


def _point_in_triangle(p, a, b, c):
    # measure area of whole triangle
    whole = abs(calc_area([a, b, c]))
    # measure areas of inner triangles formed by p
    parta = abs(calc_area([a, b, p]))
    partb = abs(calc_area([b, c, p]))
    partc = abs(calc_area([c, a, p]))
    # allow for potential rounding error in area calcs
    # (not that i've encountered one yet, but just in case...)
    thresh = 0.0000001
    # return if the sum of the inner areas = the whole area
    return (parta + partb + partc) < (whole + thresh)


def _get_ear(poly: List[int]) -> Tuple[List[int], List[int]]:
    count = len(poly)
    # not even a poly
    if count < 3:
        return [], []
    # only a triangle anyway
    if count == 3:
        return poly, []

    # start checking points
    for i in range(count):
        ia = (i - 1) % count
        ib = i
        ic = (i + 1) % count
        a = poly[ia]
        b = poly[ib]
        c = poly[ic]
        # is point b an outer corner?
        if _is_corner(a, b, c):
            # are there any other points inside triangle abc?
            valid = True
            for j, p in enumerate(poly):
                if not (j in (ia, ib, ic)):
                    if _point_in_triangle(p, a, b, c):
                        valid = False

            # if no such point found, abc must be an "ear"
            if valid:
                remaining = [p for j, p in enumerate(poly) if j != ib]
                # return the ear, and what's left of the polygon after the ear is clipped
                return [a, b, c], remaining

    # no ear was found, so something is wrong with the given poly (not anticlockwise?
    # self-intersects?)
    return [], []


def _attempt_reduction(hulla, hullb):
    inter = [vec for vec in hulla if vec in hullb]
    if len(inter) == 2:
        starta = hulla.index(inter[1])
        tempa = hulla[starta:] + hulla[:starta]
        tempa = tempa[1:]
        startb = hullb.index(inter[0])
        tempb = hullb[startb:] + hullb[:startb]
        tempb = tempb[1:]
        reduced = tempa + tempb
        if is_convex(reduced):
            return reduced
    # reduction failed, return None
    return None


def _reduce_hulls(hulls):
    count = len(hulls)
    # 1 or less hulls passed
    if count < 2:
        return hulls, False

    # check all hulls in the list against each other
    for ia in range(count - 1):
        for ib in range(ia + 1, count):
            # see if hulls can be reduced to one
            reduction = _attempt_reduction(hulls[ia], hulls[ib])
            if reduction is not None:
                # they can so return a new list of hulls and a True
                newhulls = [reduction]
                for j in range(count):
                    if not (j in (ia, ib)):
                        newhulls.append(hulls[j])
                return newhulls, True

    # nothing was reduced, send the original hull list back with a False
    return hulls, False


def triangulate(poly):
    """Triangulates poly and returns a list of triangles

    :Parameters:
        poly
            list of points that form an anticlockwise polygon
            (self-intersecting polygons won't work, results are undefined)
    """
    triangles = []
    remaining = poly[:]

    # while the poly still needs clipping
    while len(remaining) > 2:
        # rotate the list:
        # this stops the starting point from getting stale which sometimes
        # a "fan" of polys, which often leads to poor convexisation
        remaining = remaining[1:] + remaining[:1]
        # clip the ear, store it
        ear, remaining = _get_ear(remaining)
        if ear:
            triangles.append(ear)

    return triangles


def convexise(triangles):
    """Reduces a list of triangles (such as returned by triangulate()) to a
    non-optimum list of convex polygons

    :Parameters:
        triangles
            list of anticlockwise triangles (a list of three points) to reduce
    """
    # fun fact: convexise probably isn't a real word
    hulls = triangles[:]
    reduced = True
    # keep trying to reduce until it won't reduce any more
    while reduced:
        hulls, reduced = _reduce_hulls(hulls)
    # return reduced hull list
    return hulls
