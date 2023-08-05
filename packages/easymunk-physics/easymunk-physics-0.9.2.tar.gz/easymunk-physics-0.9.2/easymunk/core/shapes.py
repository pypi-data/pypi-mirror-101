import logging
from abc import abstractmethod, ABC
from math import sqrt
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Iterable,
    Generic,
    MutableMapping,
)
from weakref import WeakValueDictionary

from sidekick.properties import alias

from ..abc import CpCFFIBase, GameObjectInterface
from ..cp import ffi, lib, cp_property_, cpvec_property_, property_
from ..drawing import get_drawing_options
from ..geometry import moment_for_segment, moment_for_poly, centroid
from ..linalg import Mat22, Vec2d, vec2d_from_cffi, Transform
from ..types import (
    BB,
    ContactPointSet,
    contact_point_set_from_cffi,
    ShapeFilter,
    shape_filter_from_cffi,
    PointQueryInfo,
    SegmentQueryInfo,
)
from ..typing import VecLike, CData
from ..util import void, init_attributes

if TYPE_CHECKING:
    from .space import Space
    from .body import Body

S = TypeVar("S", bound="Shape")

SHAPE_BODY_NOTE = """It is legal to send in None as body argument to indicate that this
    shape is not attached to a body. However, you must attach it to a body
    before adding the shape to a space or used for a space shape query.
"""
SHAPE_ARGS = """
        sensor: 
            A boolean value if this shape is a sensor or not.
        collision_type: 
            Arbitrary category in associated with shape. 
        filter: 
            A collision filter object 
        elasticity: Elasticity (restitution) coefficient for collisions that 
            controls body's "bouncyness". Usually in the range 0 = no bounce 
            to 1 = perfectly elastic.  
        friction: 
            Friction coefficient.  
        surface_velocity: 
            Adds a surface velocity vector for things like conveyor belts. 
            body: body the shape is attached to.
"""

CREATED_SHAPES: MutableMapping[int, "Shape"] = WeakValueDictionary()


class Shape(GameObjectInterface, CpCFFIBase, ABC):
    """
    Base class for all the shapes.

    You usually don't want to create instances of this class directly but use
    one of the specialized shapes instead (:py:class:`Circle`,
    :py:class:`Poly` or :py:class:`Segment`).

    All the shapes can be copied and pickled. If you copy/pickle a shape the
    body (if any) will also be copied.
    """

    _pickle_kwargs = [
        "collision_type",
        "elasticity",
        "filter",
        "friction",
        "sensor",
        "surface_velocity",
    ]

    is_shape = True
    _pickle_meta_hide = {"_body", "_cffi_ref", "_nursery", "_space", "body"}
    _init_kwargs = {*_pickle_kwargs, "mass", "moment", "density", "color", "name"}
    _space: Optional["Space"] = None
    _body: Optional["Body"] = None
    _cffi_ref = None
    _id_counter = 1
    is_circle: bool = False
    is_segment: bool = False
    is_poly: bool = False
    name: Optional[str] = None
    radius: float  # All shapes define a radius, but not in the base class

    @property
    def position(self) -> Vec2d:
        return self.body.position if self.body else Vec2d(0, 0)

    @property
    @abstractmethod
    def center(self):
        raise NotImplementedError

    @property
    def center_world(self):
        """
        Center point in world coordinates.
        """
        return self.local_to_world(self.center)

    @property
    def _id(self) -> int:
        """Unique id of the Shape

        .. note::
            Experimental API. Likely to change in future major, minor or point
            releases.
        """
        return int(ffi.cast("int", lib.cpShapeGetUserData(self._cffi_ref)))

    def _set_id(self) -> int:
        counter = Shape._id_counter
        ptr = ffi.cast("cpDataPointer", counter)
        lib.cpShapeSetUserData(self._cffi_ref, ptr)
        Shape._id_counter += 1
        return counter

    mass: float = cp_property_(
        api="cpShape(Get|Set)Mass",
        doc="""The mass of this shape.

        This is useful when you let Pymunk calculate the total mass and inertia 
        of a body from the shapes attached to it. (Instead of setting the body 
        mass and inertia directly)
        """,
    )
    density: float = cp_property_(
        api="cpShape(Get|Set)Density",
        doc="""The density of this shape.
        
        This is useful when you let Pymunk calculate the total mass and inertia 
        of a body from the shapes attached to it. (Instead of setting the body 
        mass and inertia directly)
        """,
    )
    moment: float = cp_property_(
        api="cpShape(Get)Moment",
        doc="The calculated moment of this shape.",
    )
    area: float = cp_property_(
        api="cpShape(Get)Area",
        doc="The calculated area of this shape.",
    )
    center_of_gravity = cpvec_property_(
        api="cpShape(Get)CenterOfGravity",
        doc="""The calculated center of gravity of this shape.""",
    )
    sensor: bool = cp_property_(
        api="cpShape(Get|Set)Sensor",
        doc="""A boolean value if this shape is a sensor or not.

        Sensors only call collision callbacks, and never generate real
        collisions.
        """,
    )
    collision_type: int = cp_property_(
        api="cpShape(Get|Set)CollisionType",
        doc="""User defined collision type for the shape.

        See :py:meth:`Space.add_collision_handler` function for more 
        information on when to use this property.
        """,
    )
    filter: ShapeFilter
    filter = property(  # type: ignore
        lambda self: shape_filter_from_cffi(lib.cpShapeGetFilter(self._cffi_ref)),
        lambda self, f: void(lib.cpShapeSetFilter(self._cffi_ref, f)),
        doc="Set the collision :py:class:`ShapeFilter` for this shape.",
    )
    elasticity: float = cp_property_(
        api="cpShape(Get|Set)Elasticity",
        doc="""Elasticity of the shape.

        A value of 0.0 gives no bounce, while a value of 1.0 will give a
        'perfect' bounce. However due to inaccuracies in the simulation
        using 1.0 or greater is not recommended.
        """,
    )
    friction: float = cp_property_(
        api="cpShape(Get|Set)Friction",
        doc="""Friction coefficient.

        Pymunk uses the Coulomb friction model, a value of 0.0 is
        frictionless.

        A value over 1.0 is perfectly fine.

        Some real world example values from Wikipedia (Remember that
        it is what looks good that is important, not the exact value).

        ==============  ======  ========
        Material        Other   Friction
        ==============  ======  ========
        Aluminium       Steel   0.61
        Copper          Steel   0.53
        Brass           Steel   0.51
        Cast iron       Copper  1.05
        Cast iron       Zinc    0.85
        Concrete (wet)  Rubber  0.30
        Concrete (dry)  Rubber  1.0
        Concrete        Wood    0.62
        Copper          Glass   0.68
        Glass           Glass   0.94
        Metal           Wood    0.5
        Polyethene      Steel   0.2
        Steel           Steel   0.80
        Steel           Teflon  0.04
        Teflon (PTFE)   Teflon  0.04
        Wood            Wood    0.4
        ==============  ======  ========
        """,
    )
    surface_velocity = cpvec_property_(
        api="cpShape(Get|Set)SurfaceVelocity",
        doc="""The surface velocity of the object.

        Useful for creating conveyor belts or players that move around. This
        value is only used when calculating friction, not resolving the
        collision.
        """,
    )

    @property
    def body(self) -> Optional["Body"]:
        """
        The body this shape is attached to. Can be set to None to
        indicate that this shape doesnt belong to a body.
        """
        return self._body

    @body.setter
    def body(self, body: Optional["Body"]):
        if self._body is not None:
            self.detach()
        if body is not None:
            body.add_shape(self)
        self._body = body

    @property
    def bb(self) -> BB:
        """
        The bounding box :py:class:`BB` of the shape.

        Only guaranteed to be valid after :py:meth:`Shape.cache_bb` or
        :py:meth:`Space.step` is called. Moving a body that a shape is
        connected to does not update it's bounding box. For shapes used for
        queries that aren't at*tached to bodies, you can also use
        :py:meth:`Shape.update`.
        """
        ptr = lib.cpShapeGetBB(self._cffi_ref)
        return BB(ptr.l, ptr.b, ptr.r, ptr.t)

    @property
    def space(self) -> Optional["Space"]:
        """
        Get the :py:class:`Space` that shape has been added to (or None).
        """
        if (body := self.body) is not None:
            return body.space
        return None

    def __init__(
        self,
        shape: ffi.CData,
        body: Optional["Body"] = None,
        **kwargs,
    ) -> None:
        self._body = None
        self._cffi_ref = ffi.gc(shape, cffi_free_shape)
        CREATED_SHAPES[self._set_id()] = self
        init_attributes(self, self._init_kwargs, kwargs)
        if body is not None:
            body.add_shape(self)
            self._body = body

    def __getstate__(self):
        args, meta = super().__getstate__()
        if self.density:
            meta["density"] = self.density
        return args, meta

    def __repr__(self, *args):
        if args:
            (args,) = args
        name = ""
        if self.name is not None:
            name = f", name={self.name!r}"
        return f"{type(self).__name__}({args}{name})"

    def _iter_bounding_boxes(self) -> Iterable["BB"]:
        yield self.bb

    def _iter_game_object_children(self):
        yield ()

    def update_transform(self, transform: Transform) -> BB:
        """
        Update, cache and return the bounding box of a shape with an
        explicit transformation.

        Useful if you have a shape without a body and want to use it for
        querying.
        """
        ptr = lib.cpShapeUpdate(self._cffi_ref, transform)
        return BB(ptr.l, ptr.b, ptr.r, ptr.t)

    def cache_bb(self) -> BB:
        """
        Update and returns the bounding box of this shape.
        """
        ptr = lib.cpShapeCacheBB(self._cffi_ref)
        return BB(ptr.l, ptr.b, ptr.r, ptr.t)

    def reindex(self: S) -> S:
        """
        Reindex shape in space.
        """

        space = self.space
        if space is not None:
            space.reindex_shape(self)
        return self

    def point_query(self, point: VecLike) -> Optional[PointQueryInfo]:
        """
        Check if the given point lies within the shape.

        A negative distance means the point is within the shape.
        """
        ptr = ffi.new("cpPointQueryInfo *")
        _ = lib.cpShapePointQuery(self._cffi_ref, point, ptr)

        ref = int(ffi.cast("int", lib.cpShapeGetUserData(ptr.shape)))
        if ref == self._id:
            pos = Vec2d(ptr.point.x, ptr.point.y)
            grad = Vec2d(ptr.gradient.x, ptr.gradient.y)
            return PointQueryInfo(self, pos, ptr.distance, grad)
        return None

    def segment_query(
        self, start: VecLike, end: VecLike, radius: float = 0.0
    ) -> Optional[SegmentQueryInfo]:
        """
        Check if the line segment from start to end intersects the shape.

        Return query info object, if successful.
        """

        info = ffi.new("cpSegmentQueryInfo *")
        success = lib.cpShapeSegmentQuery(self._cffi_ref, start, end, radius, info)
        if success:
            ref = int(ffi.cast("int", lib.cpShapeGetUserData(info.shape)))
            if ref != self._id:
                raise RuntimeError
            pos = Vec2d(info.point.x, info.point.y)
            grad = Vec2d(info.normal.x, info.normal.y)
            return SegmentQueryInfo(self, pos, grad, info.alpha)
        return None

    def shapes_collide(self, b: "Shape") -> ContactPointSet:
        """
        Get contact information about this shape and shape b.

        It is a NO-OP if body is not in a space.
        """
        points = lib.cpShapesCollide(self._cffi_ref, b._cffi_ref)
        return contact_point_set_from_cffi(points)

    def detach(self: S) -> S:
        """
        Remove shape from body and possibly from space.
        """
        if self._body is None:
            return self
        self._body.remove_shape(self)
        return self

    def radius_of_gyration_sqr(self, axis=(0, 0)) -> float:
        """
        Radius of gyration squared.

        This is slightly more efficient than calculating radius_of_gyration()**2.
        """
        raise NotImplementedError

    def radius_of_gyration(self, axis=(0, 0)) -> float:
        """
        Radius of gyration of squared is a geometric property define as the
        radius of a ring with the same mass and moment of inertia of a body.
        """
        return sqrt(self.radius_of_gyration_sqr(axis))

    def local_to_world(self, vec: VecLike) -> Vec2d:
        """
        Convert vector from local coordinates to world coordinates.
        """
        if self.body is None:
            return Vec2d(*vec)
        return self.body.local_to_world(vec)

    def world_to_local(self, vec: VecLike) -> Vec2d:
        """
        Convert vector from world coordinates to local coordinates.
        """
        if self.body is None:
            return Vec2d(*vec)
        return self.body.world_to_local(vec)

    def step(self, dt):
        ...  # NO-OP, space takes care of that
        return self

    #
    # Game object
    #
    def draw(self, camera=None):
        camera = get_drawing_options(camera)
        camera.draw_shape(self)


class Circle(Shape):
    f"""
    A circle shape defined by a radius.

    This is the fastest and simplest collision shape.

    {SHAPE_BODY_NOTE}

    Args:
        radius: Circle radius
        offset: Center of circle with respect to the local body coordinates.
        {SHAPE_ARGS}
    """

    _pickle_args = ["radius", "offset", "body"]
    is_circle = True
    radius: float = cp_property_(
        api="cpCircleShape(Get|Set)Radius",
        doc="""The Radius of the circle
        
       .. note::
            Changes in radius are only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """,
    )
    offset = cpvec_property_(
        api="cpCircleShape(Get|Set)Offset",
        doc="""Offset. (body space coordinates)
        
        .. note::
            Changes in offset are only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """,
    )
    offset_world: Vec2d = property_(
        lambda self: self.local_to_world(self.offset),
        lambda self, o: setattr(self, "offset", o - self.position),
        doc="""Offset, in world coordinates.""",
    )
    center: Vec2d = alias("offset")

    def __init__(
        self,
        radius: float,
        offset: VecLike = (0, 0),
        body: Optional["Body"] = None,
        **kwargs,
    ) -> None:
        shape = lib.cpCircleShapeNew(cffi_body(body), radius, offset)
        super().__init__(shape, body, **kwargs)

    def __repr__(self):
        return super().__repr__(f"{self.radius}, offset={tuple(self.offset)}")

    def _iter_bounding_boxes(self) -> Iterable["BB"]:
        yield self.bb

    def radius_of_gyration_sqr(self, axis: VecLike = (0, 0)) -> float:
        """
        Return radius of gyration squared
        """
        return self.radius ** 2 / 2 + (self.offset + axis).length_sqr

    def draw(self, camera=None):
        camera = get_drawing_options(camera)
        camera.draw_circle_shape(self)


class Segment(Shape):
    f"""
    A line segment shape between two points.

    Meant mainly as a static shape. Can be beveled in order to give them a
    thickness.

    {SHAPE_BODY_NOTE}

    Args:
        a: The first endpoint of the segment
        b: The second endpoint of the segment
        radius: The thickness of the segment
        body: The body to attach the segment to
        {SHAPE_ARGS}
    """

    _pickle_args = ["a", "b", "radius", "body"]
    is_segment = True
    radius: float = cp_property_(
        "cpSegmentShape(Get|Set)Radius",
        doc="""The radius/thickness of the segment
        
       .. note::
            Changes in radius are only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """,
    )
    a = cpvec_property_(
        "cpSegmentShape(Get)A",
        lambda self, a: setattr(self, "endpoints", (a, self.b)),
        doc="The first of the two endpoints for this segment",
    )
    a_world: Vec2d
    a_world = property(  # type: ignore
        lambda self: self.position + self.a,
        lambda self, a: setattr(self, "a", a - self.position),
        doc="The first endpoint, in world coordinates",
    )
    b = cpvec_property_(
        "cpSegmentShape(Get)B",
        lambda self, b: setattr(self, "endpoints", (self.a, b)),
        doc="The second of the two endpoints for this segment",
    )
    b_world: Vec2d
    b_world = property(  # type: ignore
        lambda self: self.position + self.b,
        lambda self, b: setattr(self, "b", b - self.position),
        doc="The second endpoint, in world coordinates",
    )
    endpoints: Tuple[Vec2d, Vec2d]
    endpoints = property(  # type: ignore
        lambda self: (self.a, self.b),
        lambda self, pts: void(lib.cpSegmentShapeSetEndpoints(self._cffi_ref, *pts)),
        doc="A tuple with (a, b) endpoints.",
    )
    endpoints_world: Tuple[Vec2d, Vec2d]
    endpoints_world = property(  # type: ignore
        lambda self: (self.a_world, self.b_world),
        lambda self, pts: void(self._set_endpoints_world(*pts)),
        doc="A tuple with (a, b) endpoints.",
    )
    normal = cpvec_property_("cpSegmentShape(Get)Normal", doc="The normal")

    @property
    def center(self):
        return (self.a + self.b) * 0.5

    def __init__(
        self,
        a: VecLike,
        b: VecLike,
        radius: float,
        body: Optional["Body"] = None,
        **kwargs,
    ) -> None:
        shape = lib.cpSegmentShapeNew(cffi_body(body), a, b, radius)
        super().__init__(shape, body, **kwargs)

    def __repr__(self):
        args = f"{tuple(self.a)}, {tuple(self.b)}, radius={self.radius}"
        return super().__repr__(args)

    def _set_endpoints_world(self, a: VecLike, b: VecLike) -> None:
        pos = self.position
        lib.cpSegmentShapeSetEndpoints(self._cffi_ref, a - pos, b - pos)

    def set_neighbors(self: S, prev: VecLike, next: VecLike) -> S:
        """When you have a number of segment shapes that are all joined
        together, things can still collide with the "cracks" between the
        segments. By setting the neighbor segment endpoints you can tell
        Chipmunk to avoid colliding with the inner parts of the crack.
        """
        lib.cpSegmentShapeSetNeighbors(self._cffi_ref, prev, next)
        return self

    def radius_of_gyration_sqr(self, axis=(0, 0)) -> float:
        return moment_for_segment(1, self.a, self.b, self.radius)

    def draw(self, camera=None):
        camera = get_drawing_options(camera)
        camera.draw_segment_shape(self)


# noinspection PyIncorrectDocstring
class Poly(Shape):
    f"""
    A convex polygon shape, the slowest, but most flexible collision shape.

    A convex hull will be calculated from the vertexes automatically.

    Adding a small radius will bevel the corners and can significantly
    reduce problems where the poly gets stuck on seams in your geometry.

    It is legal to send in None as body argument to indicate that this
    shape is not attached to a body. However, you must attach it to a body
    before adding the shape to a space or used for a space shape query.


    Args:
        vertices: Define a convex hull of the polygon with a counterclockwise winding.
        radius: Set the radius of the poly shape
        transform: Transform will be applied to every vertex.
        {SHAPE_ARGS}

    .. note::
        Make sure to put the vertices around (0,0) or the shape might
        behave strange.

        Either directly place the vertices like the below example:

        >>> w, h = 10, 20
        >>> vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        >>> poly_good = mk.Poly(vs)
        >>> poly_good.center_of_gravity
        Vec2d(0.0, 0.0)

        Or use a transform to move them:

        >>> vs = [(0, 0), (w, 0), (w, h), (0, h)]
        >>> poly_bad = mk.Poly(vs)
        >>> poly_bad.center_of_gravity
        Vec2d(5.0, 10.0)
        >>> poly_good = mk.Poly(vs, transform=mk.Transform.translation(-w/2, -h/2))
        >>> poly_good.center_of_gravity
        Vec2d(0.0, 0.0)

    """

    _pickle_args = ["vertices", "radius", "body"]
    is_poly = True
    radius: float = cp_property_(
        api="cpPolyShape(Get|Set)Radius",
        doc="""The radius/thickness of polygon lines
        
       .. note::
            Changes in radius are only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """,
    )
    vertices: List[Vec2d] = property_(
        lambda self: self.get_vertices(),
        lambda self, vs: void(self.set_vertices(vs)),
    )
    vertices_world: List[VecLike] = property_(
        lambda self: self.get_vertices(world=True),
        lambda self, vs: void(self.set_vertices(vs, world=True)),
    )

    @property
    def center(self):
        return centroid(self.vertices)

    # TODO: accept offset vector in constructor
    @classmethod
    def new_box(
        cls,
        size: VecLike = (10, 10),
        radius: float = 0.0,
        body: Optional["Body"] = None,
        **kwargs,
    ) -> "Poly":
        f"""
        Convenience function to create a box given a width and height.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to.  If you want to create an off-center
        box, you will need to use the normal constructor Poly(...).

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the box gets stuck on seams in your geometry.

        Args:
            size: Size of the box as (width, height)
            radius: Radius of poly
            {SHAPE_ARGS}
        """
        poly = cls.__new__(Poly)
        shape = lib.cpBoxShapeNew(cffi_body(body), size[0], size[1], radius)
        Shape.__init__(poly, shape, body, **kwargs)
        return poly

    @classmethod
    def new_box_bb(
        cls, bb: BB, radius: float = 0.0, body: Optional["Body"] = None, **kwargs
    ) -> "Poly":
        f"""
        Convenience function to create a box shape from a :py:class:`BB`.

        The boxes will always be centered at the center of gravity of the
        body you are attaching them to.  If you want to create an off-center
        box, you will need to use the normal constructor Poly(..).

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the box gets stuck on seams in your geometry.

        Args:
            bb: Size of the box
            radius: Radius of poly
            {SHAPE_ARGS}
        """

        poly = cls.__new__(cls)
        shape = lib.cpBoxShapeNew2(cffi_body(body), bb, radius)
        Shape.__init__(poly, shape, body, **kwargs)
        return poly

    @staticmethod
    def new_regular_poly(
        n: int,
        size: float,
        radius: float = 0.0,
        body: Optional["Body"] = None,
        *,
        angle: float = 0.0,
        offset: VecLike = (0, 0),
        **kwargs,
    ) -> "Poly":
        f"""
        Convenience function to create a regular polygon of n sides of a
        given size.

        The polygon will always be centered at the center of gravity of the
        body you are attaching it to. If you want to create an off-center
        box, you will need to use the normal constructor Poly(..).

        The first vertex is in the direction of the x-axis. This can be changed
        by setting a different initial angle.

        Adding a small radius will bevel the corners and can significantly
        reduce problems where the box gets stuck on seams in your geometry.

        Args:
            n: Number of sides
            size: Length of each side
            radius: Radius of poly
            angle: Rotation angle
            offset: An offset to the center of gravity
            {SHAPE_ARGS}
        """
        vertices = regular_poly_vertices(n, size, angle, offset)
        return Poly(vertices, radius=radius, body=body, **kwargs)

    def __init__(
        self,
        vertices: Sequence[VecLike],
        radius: float = 0,
        body: Optional["Body"] = None,
        transform: Optional[Transform] = None,
        offset: Optional[VecLike] = None,
        **kwargs,
    ) -> None:
        if offset is not None:
            if transform is not None:
                raise TypeError("cannot specify transform and offset at the same time")
            transform = Transform.translation(*offset)
        elif transform is None:
            transform = Transform.identity()

        shape = lib.cpPolyShapeNew(
            cffi_body(body), len(vertices), vertices, transform, radius
        )
        super().__init__(shape, body, **kwargs)

    def __repr__(self):
        vertices = [tuple(v) for v in self.get_vertices()]
        args = f"{vertices}, radius={self.radius}"
        return super().__repr__(args)

    def get_vertices(self, *, world: bool = False) -> List[Vec2d]:
        """
        Return list of vertices in local coordinates.

        Set ``world=True`` if you need the list of vertices in world coordinates.
        """
        n = lib.cpPolyShapeGetCount(self._cffi_ref)
        vs = [
            vec2d_from_cffi(lib.cpPolyShapeGetVert(self._cffi_ref, i)) for i in range(n)
        ]
        if world and self.body is not None:
            pos = self.body.position
            rot = Mat22.rotation(self.body.angle)
            return [rot.transform(v) + pos for v in vs]
        return vs

    def set_vertices(
        self: S,
        vertices: Sequence[VecLike],
        transform: Optional[Transform] = None,
        *,
        world: bool = False,
    ) -> S:
        """
        Set the vertices of the poly.

        .. note::
            This change is only picked up as a change to the position
            of the shape's surface, but not it's velocity. Changing it will
            not result in realistic physical behavior. Only use if you know
            what you are doing!
        """
        if world and self.body is not None:
            pos = self.body.position
            rot = Mat22.rotation(-self.body.angle)
            vertices = [rot.transform(v) - pos for v in vertices]
        if transform is None:
            lib.cpPolyShapeSetVertsRaw(self._cffi_ref, len(vertices), vertices)
            return self
        lib.cpPolyShapeSetVerts(self._cffi_ref, len(vertices), vertices, transform)
        return self

    def radius_of_gyration_sqr(self, axis=(0, 0)) -> float:
        return moment_for_poly(1, self.vertices, radius=self.radius)

    def draw(self, camera=None):
        camera = get_drawing_options(camera)
        camera.draw_poly_shape(self)


Cm = TypeVar("Cm")
Sm = TypeVar("Sm")
Pm = TypeVar("Pm")


class MakeShapeMixin(ABC, Generic[Cm, Sm, Pm]):
    """
    Create shapes and possibly bodies in object.
    """

    @abstractmethod
    def _create_shape(self, cls, args, kwargs):
        raise NotImplementedError

    def create_circle(self, radius: float, offset: VecLike = (0, 0), **kwargs) -> Cm:
        """
        Create a new circle with given radius and offset.
        """
        return self._create_shape(Circle, (radius, offset), kwargs)

    def create_segment(
        self, a: VecLike, b: VecLike, radius: float = 1.0, **kwargs
    ) -> Sm:
        """
        Create a new segment from point a to point b.
        """
        return self._create_shape(Segment, (a, b, radius), kwargs)

    def create_poly(
        self,
        vertices: Iterable[VecLike],
        radius: float = 0.0,
        transform: "Transform" = None,
        **kwargs,
    ) -> Pm:
        """
        Create polygon from vertices.
        """
        kwargs["transform"] = transform
        return self._create_shape(Poly, (vertices, radius), kwargs)

    def create_box(
        self,
        shape: Tuple[float, float],
        offset: VecLike = (0, 0),
        transform: "Transform" = None,
        radius: float = 0.0,
        **kwargs,
    ) -> Pm:
        """
        Create a boxed-shaped polygon with given shape.
        """
        width, height = shape
        w, h = width / 2, height / 2
        x, y = offset
        vs = [(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)]
        return self.create_poly(vs, radius, transform, **kwargs)

    def create_box_bb(self, bb: "BB", offset: VecLike = (0, 0), **kwargs) -> Pm:
        """
        Create a boxed-shaped polygon from bounding box.
        """
        vertices = tuple(v + offset for v in BB.from_bb(bb).iter_vertices())
        return self.create_poly(vertices, **kwargs)

    def create_regular_poly(
        self, n: int, size: float, offset: VecLike = (0, 0), angle=0.0, **kwargs
    ) -> Pm:
        """
        Create a regular polygon with n sides.
        """
        vertices = regular_poly_vertices(n, size, angle, offset)
        return self.create_poly(vertices, **kwargs)


def regular_poly_vertices(
    n: int, size: float, angle: float, offset: VecLike = (0, 0)
) -> List[Vec2d]:
    """
    Return list of vertices to represent a regular polygon of size n.
    """
    u = Vec2d(size, 0).rotated(angle)
    origin = Vec2d(*offset)
    delta = 360 / n
    return [origin + u.rotated(delta * i) for i in range(n)]


def cffi_free_shape(cp_shape):
    cp_space = lib.cpShapeGetSpace(cp_shape)
    if cp_space != ffi.NULL:
        logging.debug("free %s %s", cp_space, cp_shape)
        lib.cpSpaceRemoveShape(cp_space, cp_shape)

    logging.debug("free %s", cp_shape)
    lib.cpShapeSetBody(cp_shape, ffi.NULL)
    logging.debug("free%s", cp_shape)
    lib.cpShapeFree(cp_shape)


def shape_from_cffi(ptr: ffi.CData) -> Shape:
    """
    Internal function that returns shape from cffi pointer.
    """
    if not bool(ptr):
        raise ValueError("cannot find shape from null pointer")

    id_ = int(ffi.cast("int", lib.cpShapeGetUserData(ptr)))
    try:
        return CREATED_SHAPES[id_]
    except KeyError:
        raise ValueError("Shape does not exist")


def cffi_body(body: Optional["Body"]) -> CData:
    """
    Return the C reference to body or a null pointer if body is None.
    """
    return ffi.NULL if body is None else body._cffi_ref
