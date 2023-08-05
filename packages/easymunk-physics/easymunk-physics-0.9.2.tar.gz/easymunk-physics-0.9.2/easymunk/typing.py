"""
Types, protocols and abstract base classes
"""
from typing import Union, Tuple, TYPE_CHECKING, Sequence, List, Any

if TYPE_CHECKING:
    from .linalg import Vec2d, Mat22, Transform
    from .types import BB, ShapeFilter, ContactPoint, ContactPointSet

Num = Union[int, float]

# Linear algebra
VecLike = Union[Tuple[Num, Num], "Vec2d"]
MatLike = Union["Mat22", Tuple[Num, Num, Num, Num]]
TransformLike = Union["Transform", Tuple[Num, Num, Num, Num, Num, Num]]

# Geometry
Polyline = List["Vec2d"]
PolylineLike = Union[Sequence[VecLike], Polyline]
Polylines = List[Polyline]
PolylinesLike = Union[Sequence[PolylineLike], Polylines]


# Types
BBLike = Union["BB", Tuple[Num, Num, Num, Num]]
ShapeFilterLike = Union["ShapeFilter", Tuple[int, int, int]]
ContactPointLike = Union["ContactPoint", Tuple[VecLike, VecLike, Num]]
ContactPointSetLike = Union[
    "ContactPointSet", Tuple[VecLike, Sequence[ContactPointLike]]
]

# FFI pointers
CData = Any

# Ellipsis hack (https://github.com/python/typing/issues/684)
if TYPE_CHECKING:
    from enum import Enum

    class EllipsisType(Enum):
        Ellipsis = "..."

    Ellipsis = EllipsisType.Ellipsis
else:
    EllipsisType = type(Ellipsis)
