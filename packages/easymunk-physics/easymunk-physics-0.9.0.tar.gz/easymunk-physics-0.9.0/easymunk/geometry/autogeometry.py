r"""This module contain functions for automatic generation of geometry, for
example from an image.

Example::

    >>> str = (
    ...     "xx   \n"
    ...     "xx   \n"
    ...     "     \n"
    ...     "xxxxx\n"
    ...     "xxxxx\n"
    ... )
    >>> lines = mk.march_string(str, 'x', scale=10.0)
    >>> len(lines)
    2

The information in segments can now be used to create geometry, for example as
a Poly or Segment::

    >>> s = mk.Space()
    >>> for line in lines:
    ...     a, *bs = line
    ...     for b in bs:
    ...         segment = s.static_body.create_segment(a, b, elasticity=1.0)
    ...         a = b

"""
from itertools import chain
from typing import Callable, List, Sequence, Tuple, overload, Union

from sidekick import op

from ..cp import ffi, lib
from ..types import BB
from ..linalg import Vec2d
from ..typing import VecLike

SegmentFunc = Callable[[Tuple[float, float], Tuple[float, float]], None]
SampleFunc = Callable[[Tuple[float, float]], float]
Polyline = List[VecLike]
Polylines = Sequence[Polyline]


def is_closed(polyline: Polyline) -> bool:
    """Returns true if the first vertex is equal to the last.

    Args:
        polyline: Polyline to simplify.
    """
    return bool(lib.cpPolylineIsClosed(polyline_to_cffi(polyline)))


def simplify_curves(polyline: Polyline, tolerance: float) -> List[Vec2d]:
    """Returns a copy of a polyline simplified by using the Douglas-Peucker
    algorithm.

    This works very well on smooth or gently curved shapes, but not well on
    straight edged or angular shapes.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """

    ptr = lib.cpPolylineSimplifyCurves(polyline_to_cffi(polyline), tolerance)
    simplified = []
    for i in range(ptr.count):
        v = ptr.verts[i]
        simplified.append(Vec2d(v.x, v.y))
    return simplified


def simplify_vertexes(polyline: Polyline, tolerance: float) -> List[Vec2d]:
    """
    Returns a copy of a polyline simplified by discarding "flat" vertexes.

    This works well on straight edged or angular shapes, not as well on smooth
    shapes.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """
    ptr = lib.cpPolylineSimplifyVertexes(polyline_to_cffi(polyline), tolerance)
    simplified = []
    for i in range(ptr.count):
        v = ptr.verts[i]
        simplified.append(Vec2d(v.x, v.y))
    return simplified


def to_convex_hull(polyline: Polyline, tolerance: float) -> List[Vec2d]:
    """Get the convex hull of a polyline as a looped polyline.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """
    ptr = lib.cpPolylineToConvexHull(polyline_to_cffi(polyline), tolerance)
    hull = []
    for i in range(ptr.count):
        v = ptr.verts[i]
        hull.append(Vec2d(v.x, v.y))
    return hull


def convex_decomposition(polyline: Polyline, tolerance: float) -> Polylines:
    """
    Get an approximate convex decomposition from a polyline.

    Returns a list of convex hulls that match the original shape to within
    tolerance.

    .. note::
        If the input is a self intersecting polygon, the output might end up
        overly simplified.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """
    ptr = polyline_to_cffi(polyline)
    set_ptr = lib.cpPolylineConvexDecomposition(ptr, tolerance)
    return polylines_from_cffi(set_ptr)


class PolylineSet(Sequence[Polyline]):
    """
    A set of Polylines.

    Mainly intended to be used for its :py:meth:`collect_segment` function
    when generating geometry with the :py:func:`march_soft` and
    :py:func:`march_hard` functions.
    """

    def __init__(self):
        def free(_set: ffi.CData) -> None:
            lib.cpPolylineSetFree(_set, True)

        self._cffi_ref = ffi.gc(lib.cpPolylineSetNew(), free)

    def collect_segment(self, v0: VecLike, v1: VecLike) -> None:
        """Add a line segment to a polyline set.

        A segment will either start a new polyline, join two others, or add to
        or loop an existing polyline. This is mostly intended to be used as a
        callback directly from :py:func:`march_soft` or :py:func:`march_hard`.

        Args:
            v0: Start of segment
            v1: End of segment
        """
        lib.cpPolylineSetCollectSegment(v0, v1, self._cffi_ref)

    def __str__(self):
        def render_line(ln):
            out = (f"({v.x:.1f}, {v.y:.1f})" for v in ln[:5])
            if len(ln) > 5:
                out = chain(out, ("...",))
            data = ", ".join(out)
            return f"[{data}]"

        data = (render_line(ln) for ln in polylines_from_cffi(self._cffi_ref))
        data = "".join(f"\n    {ln}" for ln in data)
        return f"{type(self).__name__}([{data}])"

    def __len__(self) -> int:
        return self._cffi_ref.count

    @overload
    def __getitem__(self, index: int) -> List[Vec2d]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "PolylineSet":
        ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise TypeError("Slice indexing not supported")
        if key >= self._cffi_ref.count:
            raise IndexError
        line = []
        ptr = self._cffi_ref.lines[key]
        for i in range(ptr.count):
            v = ptr.verts[i]
            line.append(Vec2d(v.x, v.y))
        return line


def march_soft(
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: SampleFunc,
) -> Polylines:
    """Trace an *anti-aliased* contour of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding
    box area using the sampling function and context.

    Args:
        bb: Bounding box of the area to sample within
        x_samples: Number of samples in x
        y_samples: Number of samples in y
        threshold: A higher value means more error is tolerated
        sample_func: The sample function will be called for
            x_samples * y_samples spread across the bounding box area, and
            should return a float.
    """
    return _march_fn(lib.cpMarchSoft, bb, x_samples, y_samples, threshold, sample_func)


def march_hard(
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: SampleFunc,
) -> Polylines:
    """
    Trace an *aliased* curve of an image along a particular threshold.

    The given number of samples will be taken and spread across the bounding
    box area using the sampling function and context.

    Args:
        bb: Bounding box of the area to sample within
        x_samples: Number of samples in x
        y_samples: Number of samples in y
        threshold: A higher value means more error is tolerated
        sample_func: The sample function will be called for
            x_samples * y_samples spread across the bounding box area, and
            should return a float.
    """
    return _march_fn(lib.cpMarchHard, bb, x_samples, y_samples, threshold, sample_func)


def march_string(
    src: str,
    query: Union[str, Callable[[str], bool]],
    scale: Union[float, VecLike] = 1.0,
    translate: VecLike = (0, 0),
    soft: bool = False,
    flip_y: bool = False,
    resolution: int = 1,
) -> Polylines:
    """
    Trace curves from scenario specified by string.

    Args:
        src: String specifying the scenario.
        query: Create shape from points in which the given query evaluates to
            True. If a string is passed, check if character is found in the
            string.
        scale:
            Scale factor to apply to resulting points. Accepts an scalar or
            a tuple with scale factors in x and y coordinates.
        translate:
            Translation vector to apply to resulting points.
        soft:
            If true, uses march_soft to produce anti-aliased curves.
        flip_y:
            If true, flips the scenario vertically.
        resolution:
            By default, it uses march_hard to build curve from image by encoding
            each match character as a "on" pixel and the other characters as
            "off". If different than 1, each character is treated as a group of
            resolution x resolution characters. It increases fidelity of the
            resulting curves at the cost of processing power.
    """
    lines = ["", *(f" {ln} " for ln in src.splitlines()), ""]
    if not flip_y:
        lines.reverse()
    n, m = resolution * len(src), resolution * max(map(len, lines))

    if not callable(query):
        query = op.eq(query) if len(query) == 1 else op.contains(query)

    def sample_func(pt):
        i, j = map(round, pt)
        try:
            return 1.0 if query(lines[j // resolution][i // resolution]) else 0.0
        except IndexError:
            return 0.0

    try:
        scale_x, scale_y = scale
    except TypeError:
        scale_x = scale_y = scale
    scale_x /= resolution
    scale_y /= resolution

    translate = translate - Vec2d(resolution * scale_x / 2, resolution * scale_y / 2)
    fn = march_soft if soft else march_hard
    out = []
    for ln in fn(BB(0, 0, m + 1, n + 1), m, n, 0.125, sample_func):
        ln = simplify_vertexes(ln, 0.125)
        out.append([translate + (pt.x * scale_x, pt.y * scale_y) for pt in ln])
    return out


def _march_fn(
    cp_func: callable,
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: SampleFunc,
) -> PolylineSet:
    out = PolylineSet()

    @ffi.callback("cpMarchSegmentFunc")
    def seg_cf(v0: ffi.CData, v1: ffi.CData, _data: ffi.CData) -> None:
        out.collect_segment((v0.x, v0.y), (v1.x, v1.y))

    @ffi.callback("cpMarchSampleFunc")
    def sample_cf(point: ffi.CData, _data: ffi.CData) -> float:
        return sample_func((point.x, point.y))

    cp_func(bb, x_samples, y_samples, threshold, seg_cf, ffi.NULL, sample_cf, ffi.NULL)
    return out


def polyline_to_cffi(polyline: Polyline) -> ffi.CData:
    n = len(polyline)
    ptr = ffi.new("cpPolyline *", {"verts": n})
    ptr.count = n
    ptr.capacity = n
    ptr.verts = polyline
    return ptr


def polylines_from_cffi(ptr: ffi.CData) -> List[List[Vec2d]]:
    lines = []
    for i in range(ptr.count):
        line = []
        ln = ptr.lines[i]
        for j in range(ln.count):
            v = ln.verts[j]
            line.append(Vec2d(v.x, v.y))
        lines.append(line)
    return lines
