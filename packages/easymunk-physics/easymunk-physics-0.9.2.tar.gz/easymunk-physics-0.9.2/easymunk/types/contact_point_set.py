import dataclasses
from typing import Tuple

from ..linalg import Vec2d


@dataclasses.dataclass(frozen=True)
class ContactPoint:
    """Contains information about a contact point.

    point_a and point_b are the contact position on the surface of each shape.

    distance is the penetration distance of the two shapes. Overlapping
    means it will be negative. This value is calculated as
    dot(point2 - point1), normal) and is ignored when you set the
    Arbiter.contact_point_set.
    """

    point_a: Vec2d
    point_b: Vec2d
    distance: float

    def copy(self, point_a=None, point_b=None, distance=None):
        """
        Return copy, possibly modifying some attributes.
        """
        return ContactPoint(
            point_a or self.point_a,
            point_b or self.point_b,
            self.distance if distance is None else distance,
        )


@dataclasses.dataclass(frozen=True)
class ContactPointSet:
    """Contact point sets make getting contact information simpler.

    normal is the normal of the collision

    points is the array of contact points. Can be at most 2 points.
    """

    normal: Vec2d
    points: Tuple[ContactPoint, ...]

    def copy(self, normal=None, points=None):
        """
        Return copy, possibly modifying some attributes.
        """
        return ContactPointSet(
            normal or self.normal,
            self.points if points is None else points,
        )


def contact_point_set_from_cffi(ptr) -> ContactPointSet:
    points = []
    for i in range(ptr.count):
        ps = ptr.points[i]
        a = Vec2d(ps.pointA.x, ps.pointA.y)
        b = Vec2d(ps.pointB.x, ps.pointB.y)
        points.append(ContactPoint(a, b, ps.distance))

    normal = Vec2d(ptr.normal.x, ptr.normal.y)
    return ContactPointSet(normal, tuple(points))
