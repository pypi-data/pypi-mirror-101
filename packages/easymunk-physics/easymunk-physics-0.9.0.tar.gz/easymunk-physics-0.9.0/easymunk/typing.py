"""
Types, protocols and abstract base classes
"""
from typing import Union, Tuple, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from .linalg import Vec2d, Mat22, Transform
    from .types import BB, ShapeFilter, ContactPoint, ContactPointSet

Num = Union[int, float]

# Linear algebra
VecLike = Union[Tuple[Num, Num], "Vec2d"]
MatLike = Union["Mat22", Tuple[Num, Num, Num, Num]]
TransformLike = Union["Transform", Tuple[Num, Num, Num, Num, Num, Num]]

# Types
BBLike = Union["BB", Tuple[Num, Num, Num, Num]]
ShapeFilterLike = Union["ShapeFilter", Tuple[int, int, int]]
ContactPointLike = Union["ContactPoint", Tuple[VecLike, VecLike, Num]]
ContactPointSetLike = Union[
    "ContactPointSet", Tuple[VecLike, Sequence[ContactPointLike]]
]
