from typing import NamedTuple, Sequence, List, TypeVar, TYPE_CHECKING, overload

from .mat22 import Mat22
from .math import cos, sin, sqrt
from .vec2d import Vec2d
from ..typing import VecLike

if TYPE_CHECKING:
    from ..core import Shape


class circle(NamedTuple):
    radius: float
    offset: Vec2d


ST = TypeVar("ST", bound="Shape")


class Transform(NamedTuple):
    """Type used for 2x3 affine transforms.

    See wikipedia for details:
    http://en.wikipedia.org/wiki/Affine_transformation

    The properties map to the matrix in this way:

    == == ==
     a  c  0
     b  d  0
    tx ty  1
    == == ==

    Vectors as extended with a z component of size 1, and transformed as usual.

    == == == == ==
     a  c  0     x
     b  d  0  *  y
    tx ty  1     1
    == == == == ==

    An instance can be created in this way:

        >>> Transform(1, 2, 3, 4, 5, 6)
        Transform(a=1, b=2, c=3, d=4, tx=5, ty=6)

    Or overriding only some of the values (on a identity matrix):

        >>> Transform(b=3, ty=5)
        Transform(a=1, b=3, c=0, d=1, tx=0, ty=5)

    Or using one of the static methods like identity or translation (see each
    method for details).

    """

    a: float = 1
    b: float = 0
    c: float = 0
    d: float = 1
    tx: float = 0
    ty: float = 0

    @staticmethod
    def identity() -> "Transform":
        """The identity transform

        Example:

        >>> Transform.identity()
        Transform(a=1, b=0, c=0, d=1, tx=0, ty=0)

        Returns a Transform with this matrix:

        = = =
        1 0 0
        0 1 0
        0 0 1
        = = =

        """
        return Transform(1, 0, 0, 1, 0, 0)

    @staticmethod
    def translation(x: float, y: float) -> "Transform":
        """A translation transform

        Example to translate (move) by 3 on x and 5 in y axis:

        >>> Transform.translation(3, 5)
        Transform(a=1, b=0, c=0, d=1, tx=3, ty=5)

        Returns a Transform with this matrix:

        = = =
        1 0 x
        0 1 y
        0 0 1
        = = =

        """
        return Transform(tx=x, ty=y)

    # split into scale and scale_non-uniform
    @staticmethod
    def scaling(s: float) -> "Transform":
        """A scaling transform

        Example to scale 4x:

        >>> Transform.scaling(4)
        Transform(a=4, b=0, c=0, d=4, tx=0, ty=0)

        Returns a Transform with this matrix:

        = = =
        s 0 0
        0 s 0
        0 0 1
        = = =

        """
        return Transform(a=s, d=s)

    @staticmethod
    def rotation(t: float) -> "Transform":
        """A rotation transform

        Example to rotate by 1 rad:

        >>> Transform.rotation(90)
        Transform(a=0, b=1, c=-1, d=0, tx=0, ty=0)

        Returns a Transform with this matrix:

        ====== ======= =
        cos(t) -sin(t) 0
        sin(t) cos(t)  0
        0      0       1
        ====== ======= =

        """
        c = cos(t)
        s = sin(t)
        return Transform(a=c, b=s, c=-s, d=c)

    @staticmethod
    def projection(t, translation=(0, 0)) -> "Transform":
        """
        Create a projection matrix.
        """
        return Transform.affine(Mat22.projection(t), translation)

    @staticmethod
    def affine(matrix=None, translation=(0, 0)) -> "Transform":
        """
        Create transform from linear transformation encoded in matrix and
        translation.
        """
        a, b, c, d = Mat22.identity() if matrix is None else matrix
        tx, ty = translation
        return Transform(a, b, c, d, tx, ty)

    @staticmethod
    def similarity(*, scale=None, angle=None, translation=(0, 0)) -> "Transform":
        """
        Create affine transform from similarity transformations..
        """
        if angle is not None:
            mat = Mat22.rotation(angle)
        else:
            mat = Mat22.identity()
        vec = Vec2d(*translation)

        if scale is not None:
            vec *= scale
            mat = Mat22.scale(scale) * mat

        return Transform.affine(mat, vec)

    @property
    def matrix(self) -> Mat22:
        """
        Linear component of the transform.
        """
        return Mat22(self.a, self.b, self.c, self.d)

    @property
    def vector(self) -> Vec2d:
        """
        Translation vector.
        """
        return Vec2d(self.tx, self.ty)

    def __call__(self, vec):
        return self.transform(vec)

    def __repr__(self):
        names = self._fields
        args = ", ".join(f"{k}={x:n}" for k, x in zip(names, self))
        return f"Transform({args})"

    @overload  # type: ignore[override]
    def __mul__(self, other: Mat22) -> "Transform":
        ...

    @overload
    def __mul__(self, other: "Transform") -> "Transform":
        ...

    @overload
    def __mul__(self, other: Vec2d) -> "Vec2d":
        ...

    def __mul__(self, other):
        if isinstance(other, Mat22):
            return Transform.affine(other * self.matrix, other.T * self.vector)
        elif isinstance(other, Transform):
            mat = self.matrix
            return Transform.affine(
                mat * other.matrix, self.vector + mat * other.vector
            )
        elif isinstance(other, (tuple, Vec2d)):
            return self.transform(other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Mat22):
            return Transform.affine(other * self.matrix, other * self.vector)
        return NotImplemented

    @overload  # type: ignore[override]
    def __add__(self, other: VecLike) -> Vec2d:
        ...

    @overload
    def __add__(self, other: "Transform") -> "Transform":
        ...

    def __add__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            mat = self.matrix
            return Transform.affine(mat, self.vector + mat * other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            return Transform.affine(self.matrix, self.vector + other)
        return NotImplemented

    #
    # Transform functions
    #
    def transform(self, vec: VecLike) -> Vec2d:
        """
        Return transformed vector by affine transform.
        """
        x, y = vec
        a, b, c, d, tx, ty = self
        return Vec2d(a * x + b * y + tx, c * x + d * y + ty)

    def transform_scale(self, scale: float = 1.0) -> float:
        """
        Scale factor in a similarity transform.

        This method return the correct scaling factor of similarity
        transformations. Non-similarity transformations do not have a well
        defined scaling since each direction might rescale by a different factor.
        In the later case, it returns the geometric mean of the main scaling
        directions.
        """
        return sqrt(abs(self.a * self.d - self.b * self.c)) * scale

    def transform_circle(self, radius: float, offset: VecLike = (0, 0)) -> circle:
        """
        Transform the radius and position of a circle with transform.

        General affine transformations include shear and stretch that may map
        circles onto ellipses. This mean that we cannot represent the result as
        a simple radius and position offset. This method assumes that transformation is a
        similarity transformation and produces arbitrary values otherwise.
        """
        scale = sqrt(abs(self.a * self.d - self.b * self.c))
        return circle(scale * radius, self.transform(offset))

    def transform_path(self, path: Sequence[VecLike]) -> List[Vec2d]:
        """
        Transform sequence of vectors by transform.

        This is slightly faster than applying the transform method on each
        vector separately.
        """
        a, b, c, d, tx, ty = self
        return [Vec2d(a * x + b * y + tx, c * x + d * y + ty) for (x, y) in path]

    def transform_shape(self, shape: ST) -> ST:
        """
        Transform shape by transform and return a copy.

        The copy is not bound to any space/body and keep the same properties
        of elasticity, friction, etc.

        Circles are assume a similarity transform and produce arbitrary results
        for general transformations with non-uniform stretching in any
        direction.

        Radius of polygons and segments are subject to the same considerations as
        circles.
        """
        if shape.is_circle:
            radius, offset = self.transform_circle(shape.radius, shape.offset)
            return shape.copy(radius=radius, offset=offset, body=None)

        scale = sqrt(abs(self.a * self.d - self.b * self.c))
        radius = scale * shape.radius

        if shape.is_segment:
            a, b = self.transform_path(shape.endpoints)
            return shape.copy(a=a, b=b, radius=radius, body=None)
        elif shape.is_poly:
            vertices = self.transform_path(shape.get_vertices())
            return shape.copy(vertices=vertices, radius=radius, body=None)
        else:
            cls = type(shape).__name__
            raise ValueError(f"invalid shape: {cls}")

    #
    # Mathematical properties
    #
    def is_similarity(self, tol=1e-9):
        """
        Return True if it is a similarity transformation given the numerical
        tolerance.
        """
        # Absolute value of determinant must be equal to one (unitary transform)
        if abs(abs(self.a * self.d - self.b * self.c) - 1) > tol:
            return False
        return True

    def is_linear(self, tol=1e-9):
        """
        Return True if transformation is purely linear in the given numeric
        tolerance.

        Translations make affine transformations non-linear.
        """
        if tol == 0:
            return self.tx == self.ty == 0.0
        return abs(self.tx) < tol and abs(self.ty) < tol
