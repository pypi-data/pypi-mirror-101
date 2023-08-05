"""
This module contain the Vec2d class that is used in all of easymunk when a
vector is needed.

The Vec2d class is used almost everywhere in easymunk for 2d coordinates and
vectors, for example to define position vector in a Body. However, easymunk is
smart enough to convert tuples to Vec2ds so you usually do not need to
explicitly do conversions if you happen to have a tuple.
"""
import numbers
from math import cos as _rcos, sin as _rsin
from typing import (
    NamedTuple,
    Tuple,
    Any,
    overload,
    TYPE_CHECKING,
    Sequence,
    Type,
)

from .math import (
    sqrt,
    atan2,
    cos,
    sin,
    radians as _radians,
    degrees as _degrees,
    isfinite,
    isnan,
)
from ..typing import Num, VecLike


class Vec2d(NamedTuple):
    """2d vector class, supports vector and scalar operators, and also
    provides some high level functions.
    """

    x: float
    y: float

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @classmethod
    def from_coords(cls, obj: Sequence) -> "Vec2d":
        """
        Create Vec2d from 2-sequence of (x, y) coordinates.

        This is useful to normalize input tuples into Vec2d instances.

        >>> Vec2d.from_coords((1, 2))
        Vec2d(1, 2)

        This is a no-op for Vec2d inputs

        >>> u = Vec2d(1, 2)
        >>> Vec2d.from_coords(u) is u
        True
        """
        if obj.__class__ is cls:
            return obj  # type: ignore
        try:
            return cls(*obj)
        except TypeError:
            pass

        try:
            return cls(obj.x, obj.y)  # type: ignore
        except AttributeError:
            raise TypeError(f"invalid vec-like type: {type(obj).__name__}")

    @classmethod
    def from_displacement(cls: Type["Vec2d"], a: VecLike, b: VecLike) -> "Vec2d":
        """
        Create Vec2d from displacement a - b.

        >>> Vec2d.from_displacement((1, 2), (3, 4))
        Vec2d(-2, -2)
        """
        x, y = a
        u, v = b
        return cls(x - u, y - v)

    @staticmethod
    def polar(angle=0.0, r=1.0) -> "Vec2d":
        """
        Create vector from polar coordinates passing its angle and length.

        Args:
            angle: Angle in degrees
            r: Length of resulting vector.

        >>> Vec2d.polar(90)
        Vec2d(0, 1)
        """
        return Vec2d(r * cos(angle), r * sin(angle))

    @staticmethod
    def polar_radians(radians=0.0, r=1.0) -> "Vec2d":
        """
        Create vector from polar coordinates, with angle given in radians.

        >>> Vec2d.polar_radians(pi / 4)
        Vec2d(0.707107, 0.707107)
        """
        return Vec2d(r * _rcos(radians), r * _rsin(radians))

    @staticmethod
    def zero() -> "Vec2d":
        """A vector of zero length.

        >>> Vec2d.zero()
        Vec2d(0, 0)
        """
        return Vec2d(0.0, 0.0)

    @staticmethod
    def ux() -> "Vec2d":
        """A unit basis vector pointing right.

        >>> Vec2d.ux()
        Vec2d(1, 0)
        """
        return Vec2d(1.0, 0.0)

    @staticmethod
    def uy() -> "Vec2d":
        """A unit basis vector pointing up.

        >>> Vec2d.uy()
        Vec2d(0, 1)
        """
        return Vec2d(0.0, 1.0)

    @property
    def length_sqr(self) -> float:
        """Squared length of vector.

        If the squared length is enough it is more efficient to use this method
        instead of access .length and then do a x**2.

        >>> v = Vec2d(3, 4)
        >>> v.length_sqr == v.length ** 2 == 25.0
        True
        """
        return self.x ** 2 + self.y ** 2

    @property
    def length(self) -> float:
        """Length of vector.

        >>> Vec2d(3, 4).length
        5.0
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self) -> float:
        """The angle (in degrees) of the vector"""
        if self.length_sqr == 0:
            return 0
        return atan2(self.y, self.x)

    @property
    def radians(self) -> float:
        """The angle (in radians) of the vector"""
        return _radians(self.angle)

    @property
    def is_finite(self):
        """True if both components are finite non-nan numbers."""
        x, y = self
        return isfinite(x) and isfinite(y)

    @property
    def is_nan(self):
        """True if any of the components is NaN"""
        x, y = self
        return isnan(x) and isnan(y)

    # PyCharm's type check sometimes get confused by constructor signatures.
    def __new__(cls, x: Num, y: Num):  # type: ignore
        new = tuple.__new__(cls, (x, y))
        return new

    def __init__(self, x: Num, y: Num):  # type: ignore
        tuple.__init__(self)

    if not TYPE_CHECKING:  # type: ignore
        del __init__
        del __new__

    def __repr__(self) -> str:
        x, y = self
        return f"Vec2d({x:n}, {y:n})"

    @overload  # type: ignore[override]
    def __add__(self, other: "Vec2d") -> "Vec2d":
        ...

    @overload
    def __add__(self, other: VecLike) -> "Vec2d":
        ...

    def __add__(self, other):
        try:
            u, v = other
        except (IndexError, TypeError):
            return NotImplemented
        else:
            return Vec2d(self.x + u, self.y + v)

    def __radd__(self, other: VecLike) -> "Vec2d":
        return self.__add__(other)

    def __sub__(self, other: VecLike) -> "Vec2d":
        try:
            u, v = other
        except (IndexError, TypeError):
            return NotImplemented
        else:
            return Vec2d(self.x - u, self.y - v)

    def __rsub__(self, other: VecLike) -> "Vec2d":
        try:
            u, v = other
        except (IndexError, TypeError):
            return NotImplemented
        else:
            return Vec2d(u - self.x, v - self.y)

    def __mul__(self, other: float) -> "Vec2d":
        if other.__class__ is float or isinstance(other, numbers.Real):
            return Vec2d(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: float) -> "Vec2d":
        return self.__mul__(other)

    def __floordiv__(self, other: float) -> "Vec2d":
        if other.__class__ is float or isinstance(other, numbers.Real):
            return Vec2d(self.x // other, self.y // other)
        return NotImplemented

    def __truediv__(self, other: float) -> "Vec2d":
        if other.__class__ is float or isinstance(other, numbers.Real):
            return Vec2d(self.x / other, self.y / other)
        return NotImplemented

    def __neg__(self) -> "Vec2d":
        return Vec2d(-self.x, -self.y)

    def __pos__(self) -> "Vec2d":
        return Vec2d(+self.x, +self.y)

    def __abs__(self) -> float:
        return self.length

    def scale_to_length(self, length: float) -> "Vec2d":
        """Return a copy of this vector scaled to the given length.

        >>> Vec2d(3, 4).scale_to_length(10)
        Vec2d(6, 8)
        """
        old_length = self.length
        return Vec2d(self.x * length / old_length, self.y * length / old_length)

    def rotated(self, angle: float) -> "Vec2d":
        """
        Create and return a new vector by rotating this vector by
        angle (in degrees).
        """
        cos_ = cos(angle)
        sin_ = sin(angle)
        x = self.x * cos_ - self.y * sin_
        y = self.x * sin_ + self.y * cos_
        return Vec2d(x, y)

    def rotated_radians(self, radians: float) -> "Vec2d":
        """
        Create and return a new vector by rotating this vector by
        angle (in radians).
        """
        return self.rotated(_degrees(radians))

    def angle_between(self, other: VecLike) -> float:
        """Get the angle between the vector and the other in degrees."""
        u, v = other
        cross = self.x * v - self.y * u
        dot = self.x * u + self.y * v
        return atan2(cross, dot)

    def radians_between(self, other: VecLike) -> float:
        """Get the angle between the vector and the other in radians."""
        return _radians(self.angle_between(other))

    def normalized(self) -> "Vec2d":
        """
        Get a normalized copy of the vector

        Note:
            This function will return 0 if the length of the vector is 0.
        """
        length = self.length
        if length != 0:
            return self / length
        return Vec2d(0, 0)

    def normalized_and_length(self) -> Tuple["Vec2d", float]:
        """
        Normalize the vector and return its length before the normalization
        """
        length = self.length
        if length != 0:
            return self / length, length
        return Vec2d(0, 0), 0

    def perpendicular(self) -> "Vec2d":
        """
        Return a perpendicular vector rotated by 90 degrees counterclockwise.
        """
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self) -> "Vec2d":
        """
        Return a normalized perpendicular vector.

        Rotate counterclockwise.
        """
        length = self.length
        if length != 0:
            return Vec2d(-self.y / length, self.x / length)
        return Vec2d(self.x, self.y)

    def dot(self, other: VecLike) -> float:
        """The dot product between the vector and other vector

        u.dot(v) -> u.x * v.x + u.y * v.y
        """
        u, v = other
        return float(self.x * u + self.y * v)

    def distance(self, other: VecLike) -> float:
        """The distance between the vector and other vector."""
        u, v = other
        return sqrt((self.x - u) ** 2 + (self.y - v) ** 2)

    def distance_sqr(self, other: VecLike) -> float:
        """The squared distance between the vector and other vector.

        It is more efficient to use this method than to call get_distance()
        first and then do a sqrt() on the result.
        """
        u, v = other
        return (self.x - u) ** 2 + (self.y - v) ** 2

    def projection(self, other: VecLike) -> "Vec2d":
        """Project this vector on top of other vector"""

        u, v = other
        other_length_sqrd = u * u + v * v
        if other_length_sqrd == 0.0:
            return Vec2d(0, 0)
        projected_length_times_other_length = self.dot(other)
        new_length = projected_length_times_other_length / other_length_sqrd
        return Vec2d(u * new_length, v * new_length)

    def cross(self, other: VecLike) -> float:
        """The cross product between the vector and other vector

        u.cross(v) -> u.x * v.y - v.y * u.x
        """
        u, v = other
        return self.x * v - self.y * u

    def interpolate_to(self, other: VecLike, ratio: float = 0.5) -> "Vec2d":
        """Interpolate with other vector.

        The "ratio" parameter determines the weight of self and other. If ratio=0,
        returns self and ratio=1 returns other. Intermediate values produce
        intermediate vectors.
        """
        u, v = other
        return Vec2d(self.x + (u - self.x) * ratio, self.y + (v - self.y) * ratio)

    def convert_to_basis(self, x_vector: VecLike, y_vector: VecLike) -> "Vec2d":
        """
        Compute coordinates from pair of basis vectors.
        """
        return Vec2d(
            self.dot(x_vector) / Vec2d(*x_vector).length_sqr,
            self.dot(y_vector) / Vec2d(*y_vector).length_sqr,
        )

    # Extra functions, mainly for chipmunk
    def complex_rotation(self, other: VecLike) -> "Vec2d":
        """
        Uses complex multiplication to rotate this vector by the other.

        Complex multiplication multiply lengths and add angles.
        """
        u, v = other
        return Vec2d(self.x * u - self.y * v, self.x * v + self.y * u)

    def cpvunrotate(self, other: VecLike) -> "Vec2d":
        """
        Uses complex multiplication to rotate this vector by the conjugate of
        other.

        Complex multiplication multiply lengths and add angles. The conjugate
        operation simply swaps the sign of the angle.
        """
        u, v = other
        return Vec2d(self.x * u + self.y * v, self.y * u - self.x * v)

    def copy(self, x=None, y=None) -> "Vec2d":
        """
        Return a copy, possibly changing x or y coordinates.
        """
        return Vec2d(x or self.x, y or self.y)

    @overload
    def round(self) -> Tuple[int, int]:
        ...

    @overload
    def round(self, prec: int) -> Tuple[float, float]:
        ...

    def round(self, prec=None):
        """
        The x and y values of this vector as a tuple of ints.
        Uses round() to round to closest int.

        >>> Vec2d(0.9, 2.4).round()
        (1, 2)
        """
        return round(self.x, prec), round(self.y, prec)

    def trunc(self) -> Tuple[int, int]:
        """
        The x and y values of this vector as a tuple of ints.

        Uses int() to discard the decimal part of number.

        >>> Vec2d(0.9, 2.4).trunc()
        (0, 2)
        """
        return int(self.x), int(self.y)

    def clamp(self, min: float = 0.0, max: float = float("inf")) -> "Vec2d":
        """
        Clamp vector to minimum and maximum length.

        Args:
            min: minimum length of vector.
            max: maximum length of vector.
        """
        size = self.length
        if min <= size <= max:
            return self

        n = self.normalized()
        return n * min if size < min else n * max

    def simeq(self, other: VecLike, abs: float = 1e-6, rel: float = 1e-6) -> bool:
        """
        Tests if both vectors a approximately equal given either some relative
        or absolute tolerance. NaN components are also evaluated as equal.

        Vectors are considered to be equal if difference falls under any of the
        given absolute or relative tolerances.

        Args:
            other: other vector to test.
            abs: Absolute tolerance
            rel: Relative tolerance

        >>> Vec2d(1, 2).simeq((1.25, 1.75), abs=0.25)
        True
        """
        x, y = self
        u, v = other
        return simeq(x, u, abs, rel) and simeq(y, v, abs, rel)


def simeq(a: float, b: float, abs: float = 1e-6, rel: float = 1e-6):
    """
    Verify if a and b are almost equal.
    """

    if a == b:
        return True

    diff = _abs(a - b)

    if isnan(diff):
        return isnan(a) and isnan(b)

    if diff <= abs:
        return True
    try:
        ratio = a / b
    except ZeroDivisionError:
        return a == 0

    return ratio > 0 and _abs(ratio - 1) <= rel


# TODO: remove these and use only Vec2d.from_coords?
def vec2d_from_cffi(cffi: Any) -> Vec2d:
    """
    Creates Vec2d from cffi cpVect.
    """
    return Vec2d(cffi.x, cffi.y)


def as_vec(v: VecLike) -> Vec2d:
    """
    Convert any VecLike to Vec2d.
    """
    if isinstance(v, Vec2d):
        return v
    return Vec2d(*v)


_abs = abs
