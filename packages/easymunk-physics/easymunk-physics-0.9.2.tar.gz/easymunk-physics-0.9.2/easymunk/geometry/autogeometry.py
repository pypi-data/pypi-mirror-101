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
import operator as op
from functools import partial
from typing import Callable, Tuple, Union

from ..cp import lib, ffi
from ..linalg import Vec2d
from ..types import BB
from ..typing import VecLike, Polyline, PolylineLike, Polylines, CData

SegmentFunc = Callable[[VecLike, VecLike], None]
SampleFunc = Callable[[VecLike], float]
Scale = Union[float, VecLike]


def is_closed(polyline: PolylineLike) -> bool:
    """Returns true if the first vertex is equal to the last.

    Args:
        polyline: Polyline to simplify.
    """
    return bool(lib.cpPolylineIsClosed(polyline_to_cffi(polyline)))


def separate_scale(scale: Scale) -> Tuple[float, float]:
    """
    Separate scale parameter in x and y components.
    """
    try:
        x, y = scale  # type: ignore
        return x, y
    except TypeError:
        return scale, scale  # type: ignore


def simplify_curves(polyline: PolylineLike, tolerance: float) -> Polyline:
    """Returns a copy of a polyline simplified by using the Douglas-Peucker
    algorithm.

    This works very well on smooth or gently curved shapes, but not well on
    straight edged or angular shapes.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """

    ptr = lib.cpPolylineSimplifyCurves(polyline_to_cffi(polyline), tolerance)
    return polyline_from_cffi(ptr)


def simplify_vertexes(polyline: PolylineLike, tolerance: float) -> Polyline:
    """
    Returns a copy of a polyline simplified by discarding "flat" vertexes.

    This works well on straight edged or angular shapes, not as well on smooth
    shapes.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """
    ptr = lib.cpPolylineSimplifyVertexes(polyline_to_cffi(polyline), tolerance)
    return polyline_from_cffi(ptr)


def to_convex_hull(polyline: PolylineLike, tolerance: float) -> Polyline:
    """Get the convex hull of a polyline as a looped polyline.

    Args:
        polyline: Polyline to simplify.
        tolerance: A higher value means more error is tolerated.
    """
    ptr = lib.cpPolylineToConvexHull(polyline_to_cffi(polyline), tolerance)
    return polyline_from_cffi(ptr)


def convex_decomposition(polyline: PolylineLike, tolerance: float) -> Polylines:
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
    ptr = lib.cpPolylineConvexDecomposition(polyline_to_cffi(polyline), tolerance)
    return polylines_from_cffi(ptr)


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
    scale: Scale = 1.0,
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
        query = (
            partial(op.eq, query) if len(query) == 1 else partial(op.contains, query)
        )

    def sample_func(pt):
        i, j = map(round, pt)
        try:
            return 1.0 if query(lines[j // resolution][i // resolution]) else 0.0
        except IndexError:
            return 0.0

    scale_x, scale_y = separate_scale(scale)
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
    cp_func: Callable,
    bb: "BB",
    x_samples: int,
    y_samples: int,
    threshold: float,
    sample_func: SampleFunc,
) -> Polylines:
    ptr: CData = ffi.gc(lib.cpPolylineSetNew(), free_polyline_set)

    @ffi.callback("cpMarchSegmentFunc")
    def segment_fn(v0: CData, v1: CData, _) -> None:
        lib.cpPolylineSetCollectSegment(v0, v1, ptr)

    @ffi.callback("cpMarchSampleFunc")
    def sample_fn(pt: CData, _) -> float:
        return sample_func((pt.x, pt.y))

    data = ffi.NULL
    cp_func(bb, x_samples, y_samples, threshold, segment_fn, data, sample_fn, data)
    return polylines_from_cffi(ptr)


def polyline_to_cffi(polyline: PolylineLike) -> ffi.CData:
    ptr = ffi.new("cpPolyline *", {"verts": (n := len(polyline))})
    ptr.count = n
    ptr.capacity = n
    ptr.verts = polyline
    return ptr


def polyline_from_cffi(ptr: CData) -> Polyline:
    return [Vec2d(v.x, v.y) for i in range(ptr.count) if (v := ptr.verts[i])]


def polylines_from_cffi(ptr: CData) -> Polylines:
    return [polyline_from_cffi(ptr.lines[i]) for i in range(ptr.count)]


def free_polyline_set(ptr: ffi.CData) -> None:
    lib.cpPolylineSetFree(ptr, True)
