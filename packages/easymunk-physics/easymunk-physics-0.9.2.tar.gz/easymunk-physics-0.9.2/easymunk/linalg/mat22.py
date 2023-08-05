from numbers import Real
from typing import Union, Tuple, Iterable, NamedTuple, List, cast, overload

from .math import sqrt, cos, sin
from .vec2d import Vec2d
from ..typing import VecLike, MatLike, Num


class Mat22(NamedTuple):
    """
    A 2x2 matrix.

    Support basic algebraic operations and exposes matrix properties as methods.

    Matrices are represented as:

    = =
    a c
    b d
    = =
    """

    a: float
    b: float
    c: float
    d: float

    @staticmethod
    def identity() -> "Mat22":
        """
        New identity matrix.
        """
        return Mat22.scale(1, 1)

    @staticmethod
    def rotation(angle: float) -> "Mat22":
        """
        Return a rotation matrix for the given angle.
        """
        cos_ = cos(angle)
        sin_ = sin(angle)
        return Mat22(cos_, sin_, -sin_, cos_)

    @staticmethod
    def projection(angle: float) -> "Mat22":
        """
        Return the projection matrix in the given direction.
        """
        cos_ = cos(angle)
        sin_ = sin(angle)
        diag = cos_ * sin_
        return Mat22(cos_ ** 2, diag, diag, sin_ ** 2)

    @staticmethod
    def scale(scale_x, scale_y=None) -> "Mat22":
        """
        Return a scale matrix.

        Pass two arguments to define different scales for the x and y
        coordinates.
        """
        if scale_y is None:
            scale_y = scale_x
        return Mat22(scale_x, 0, 0, scale_y)

    @staticmethod
    def zero() -> "Mat22":
        """
        Return the null matrix
        """
        return Mat22(0.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_rows(rows: List[VecLike]) -> "Mat22":
        """
        Create matrix from list of rows
        """
        r1, r2 = rows
        a, c = r1
        b, d = r2
        return Mat22(a, b, c, d)

    @property
    def trace(self) -> float:
        """
        Matrix trace.
        """
        return self.a + self.d

    @property
    def determinant(self) -> float:
        """
        Matrix determinant.
        """
        return self.a * self.d - self.b * self.c

    # noinspection PyPep8Naming
    @property
    def T(self) -> "Mat22":
        """
        Transpose matrix.
        """
        return self.transposed()

    @property
    def eigenvalues(self) -> Tuple[complex, complex]:
        """
        A 2-tuple with matrix eigenvalues.
        """
        a, b, c, d = self
        aux = d ** 2 - 2 * a * d + a ** 2 + 4 * c * b
        aux_ = cast(complex, sqrt(aux)) if aux >= 0 else sqrt(-aux) * 1j
        return (d + a + aux_) / 2, (d + a - aux_) / 2

    @property
    def eigenvectors(self) -> Tuple[Tuple[complex, complex], Tuple[complex, complex]]:
        """
        A 2-tuple with normalized eigenvectors.
        """
        l1, l2 = self.eigenvalues
        v1 = self.c / (l1 - self.a), 1
        v2 = self.c / (l2 - self.a), 1
        return normalized(v1), normalized(v2)

    def __repr__(self):
        return f"Mat22({self.a}, {self.b}, {self.c}, {self.d})"

    def __str__(self):
        return f"|{self.a}, {self.b}|\n|{self.c}, {self.d}|"

    @overload  # type: ignore[override]
    def __add__(self, other: "Mat22") -> "Mat22":
        ...

    @overload
    def __add__(self, other: MatLike) -> "Mat22":
        ...

    def __add__(self, other):
        if isinstance(other, Mat22):
            a, b, c, d = self
            x, y, z, w = other
            return Mat22(a + x, b + y, c + z, d + w)
        elif isinstance(other, tuple):
            return self + as_mat2(other)
        return NotImplemented

    def __sub__(self, other: "Mat22") -> "Mat22":
        if isinstance(other, Mat22):
            a, b, c, d = self
            x, y, z, w = other
            return Mat22(a - x, b - y, c - z, d - w)
        return NotImplemented

    def _real_mul(self, other: Real) -> "Mat22":
        r = float(other)
        a, b, c, d = self
        return Mat22(a * r, b * r, c * r, d * r)

    def _mat_mul(self, other: "Mat22") -> "Mat22":
        a, b, c, d = self
        x, y, z, w = other
        return Mat22(a * x + b * z, a * y + b * w, c * x + b * z, c * y + d * w)

    def __matmul__(self, other):
        if isinstance(other, Mat22):
            return self._mat_mul(other)
        return NotImplemented

    @overload  # type: ignore[override]
    def __mul__(self, other: Num) -> "Mat22":
        ...

    @overload
    def __mul__(self, other: "Mat22") -> "Mat22":
        ...

    @overload
    def __mul__(self, other: "Vec2d") -> "Vec2d":
        ...

    def __mul__(self, other):
        if isinstance(other, Mat22):
            return self._mat_mul(other)
        elif isinstance(other, Real):
            return self._real_mul(other)
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self.transform(cast(VecLike, other))
            return NotImplemented
        return NotImplemented

    def __rmul__(self, other) -> "Mat22":
        if isinstance(other, Real):
            return self._real_mul(other)
        return NotImplemented

    def __truediv__(self, other):
        return self._real_mul(1 / other)

    def __getitem__(self, idx):
        if idx == 0:
            return Vec2d(self.a, self.c)
        elif idx == 1:
            return Vec2d(self.b, self.d)
        elif idx == (0, 0):
            return self.a
        elif idx == (0, 1):
            return self.c
        elif idx == (1, 0):
            return self.b
        elif idx == (1, 1):
            return self.d
        raise IndexError(idx)

    def copy(self, **kwargs) -> "Mat22":
        """
        Return copy possibly replacing some coordinate.
        """
        kwargs.setdefault("a", self.a)
        kwargs.setdefault("b", self.b)
        kwargs.setdefault("c", self.c)
        kwargs.setdefault("d", self.d)
        return Mat22(**kwargs)

    def rows(self) -> Iterable[Vec2d]:
        """
        Iterate over row vectors.
        """
        yield Vec2d(self.a, self.c)
        yield Vec2d(self.b, self.d)

    def cols(self) -> Iterable[Vec2d]:
        """
        Iterate over column vectors.
        """
        yield Vec2d(self.a, self.b)
        yield Vec2d(self.c, self.d)

    def interpolate_to(self, other: MatLike, ratio: float = 0.5) -> "Mat22":
        """
        Linear interpolation of matrix with "other".

        Ratio controls the weight given to each point in the interpolation.
        In the extremes, if range=0.0, it returns self, range=1.0 returns other.
        """
        m1 = self * (1 - ratio)
        m2 = as_mat2(other) * ratio
        return m1 + m2

    def inverse(self) -> "Mat22":
        """
        Return the inverse matrix::

            M.inverse() * M = Mat22.identity()
        """
        det = self.determinant
        return Mat22(self.d / det, -self.b / det, -self.c / det, self.a / det)

    def rotate(self, angle: float) -> "Mat22":
        """
        Apply rotation by the given angle.

        This is the same as ``R * M * R.inverse()``.
        """
        a, b, c, d = self
        c = cos(angle)
        s = sin(angle)
        cs = c * s
        c2 = c * c
        return Mat22(
            (a - d) * c2 + d - cs * (b + c),
            (c - b) * c2 - c + cs * (a + d),
            (c + b) * c2 - b + cs * (a - d),
            (d - a) * c2 + a + cs * (b + c),
        )

    def transform(self, vec: VecLike) -> Vec2d:
        """
        Return a the result of applying the linear transformation to vec.
        """
        x, y = vec
        return Vec2d(self.a * x + self.c * y, self.b * x + self.d * y)

    def transposed(self) -> "Mat22":
        """
        Return transposed matrix.
        """
        return Mat22(self.a, self.c, self.b, self.d)


def as_mat2(obj: Union[Mat22, tuple, list]) -> Mat22:
    """
    Convert object to Mat22, if necessary.
    """
    if isinstance(obj, Mat22):
        return obj
    elif isinstance(obj, (tuple, list)):
        if len(obj) == 2:
            (a, c), (b, d) = obj
            return Mat22(a, b, c, d)
        else:
            return Mat22(*obj)

    kind = type(obj).__name__
    raise TypeError(f"cannot convert {kind} to Mat22")


def normalized(vec: Tuple[complex, complex]) -> Tuple[complex, complex]:
    x, y = vec
    norm = sqrt((x * x.conjugate() + y * y.conjugate()).real)
    return x / norm, y / norm
