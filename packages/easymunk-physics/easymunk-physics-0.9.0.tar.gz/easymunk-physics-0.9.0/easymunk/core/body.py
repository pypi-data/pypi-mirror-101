import logging
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Set,
    TypeVar,
    Union,
    Tuple,
    List,
    Iterator,
    cast,
    Literal,
    overload,
)
from weakref import WeakValueDictionary

import sidekick.api as sk

from .arbiter import Arbiter
from .constraints import (
    Constraint,
    PositionJoint,
    DistanceJoint,
    LimitDistanceJoint,
    SegmentJoint,
    DampedSpring,
    RatchetJoint,
    LimitAngleJoint,
    DampedRotarySpring,
    AngularVelocityJoint,
    ConstraintOpts,
    ConstraintKwargs,
)
from .junction import Junction
from .shapes import Shape, Circle, Poly, Segment, MakeShapeMixin
from ..abc import GameObjectInterface, HasBBMixin, CpCFFIBase
from ..cp import cpvec_property, cp_property, lib, ffi
from ..drawing import get_drawing_options
from ..geometry import centroid
from ..linalg import Vec2d, Transform
from ..typing import VecLike
from ..linalg.math import (
    degrees as to_degrees,
    radians as to_radians,
    isfinite,
    isnan,
    degrees,
)
from ..types import Shapes, Constraints
from ..util import void, set_attrs, init_attributes

if TYPE_CHECKING:
    from ..types import ShapeFilter, BB
    from .space import Space

# Types
T = TypeVar("T")
BodyT = TypeVar("BodyT", bound="Body")
BodyType = Union[Literal["static", "dynamic", "kinematic"], int]
PositionFuncT = Callable[[BodyT, float], None]
VelocityFuncT = Callable[[BodyT, Vec2d, float, float], None]
AxisT = Union[VecLike, Literal["center", "top"], None]
ConsT = TypeVar("ConsT", bound=Constraint)

# Constants
BODY_TYPES = {}
CREATED_BODIES = WeakValueDictionary()
CONSTRAINT_KWARGS_DOC = ConstraintOpts.__doc__


class Body(
    MakeShapeMixin[Circle, Segment, Poly], GameObjectInterface, CpCFFIBase, HasBBMixin
):
    """A rigid body

    * Use forces to modify the rigid bodies if possible. This is likely to be
      the most stable.
    * Modifying a body's velocity shouldn't necessarily be avoided, but
      applying large changes can cause strange results in the simulation.
      Experiment freely, but be warned.
    * Don't modify a body's position every step unless you really know what
      you are doing. Otherwise you're likely to get the position/velocity badly
      out of sync.

    A Body can be copied and pickled. Sleeping bodies that are copied will be
    awake in the fresh copy. When a Body is copied any spaces, shapes or
    constraints attached to the body will not be copied.

    Args:
        mass:
            Body mass. Mass and moment are ignored when body_type is "kinematic"
            or "static".
        moment:
            Body moment. Analogous to rotational mass.
        body_type:
            Determines the body type, can be "dynamic", "kinematic" or "static".

    Notes:
        Guessing the mass for a body is usually fine, but guessing a moment
        of inertia can lead to a very poor simulation so it's recommended to
        use Chipmunk's moment calculations to estimate the moment for you.

        There are two ways to set up a dynamic body. The easiest option is to
        create a body with a mass and moment of 0, and set the mass or
        density of each collision shape added to the body. Chipmunk will
        automatically calculate the mass, moment of inertia, and center of
        gravity for you. This is probably preferred in most cases. Note that
        these will only be correctly calculated **after** the body and shape are
        added to a space.

        The other option is to set the mass of the body when it's created,
        and leave the mass of the shapes added to it as 0.0. This approach is
        more flexible, but is not as easy to use. Don't set the mass of both
        the body and the shapes. If you do so, it will recalculate and
        overwrite your custom mass value when the shapes are added to the body.
    """

    DYNAMIC = BODY_TYPES["dynamic"] = lib.CP_BODY_TYPE_DYNAMIC
    """Dynamic bodies are the default body type.

    They react to collisions,
    are affected by forces and gravity, and have a finite amount of mass.
    These are the type of bodies that you want the physics engine to
    simulate for you. Dynamic bodies interact with all types of bodies
    and can generate collision callbacks.
    """

    KINEMATIC = BODY_TYPES["kinematic"] = lib.CP_BODY_TYPE_KINEMATIC
    """Kinematic bodies are bodies that are controlled from your code
    instead of inside the physics engine.

    They arent affected by gravity and they have an infinite amount of mass
    so they don't react to collisions or forces with other bodies. Kinematic
    bodies are controlled by setting their velocity, which will cause them
    to move. Good examples of kinematic bodies might include things like
    moving platforms. Objects that are touching or jointed to a kinematic
    body are never allowed to fall asleep.
    """

    STATIC = BODY_TYPES["static"] = lib.CP_BODY_TYPE_STATIC
    """Static bodies are bodies that never (or rarely) move.

    Using static bodies for things like terrain offers a big performance
    boost over other body types- because Chipmunk doesn't need to check for
    collisions between static objects and it never needs to update their
    collision information. Additionally, because static bodies don't
    move, Chipmunk knows it's safe to let objects that are touching or
    jointed to them fall asleep. Generally all of your level geometry
    will be attached to a static body except for things like moving
    platforms or doors. Every space provide a built-in static body for
    your convenience. Static bodies can be moved, but there is a
    performance penalty as the collision information is recalculated.
    There is no penalty for having multiple static bodies, and it can be
    useful for simplifying your code by allowing different parts of your
    static geometry to be initialized or moved separately.
    """

    is_body = True
    _pickle_args = "mass", "moment", "body_type"
    _pickle_kwargs = (
        # Arguments not included in init_args
        "force",
        "torque",
        # Init args arguments
        "angle",
        "angular_velocity",
        "center_of_gravity",
        "position",
        "velocity",
    )
    _pickle_meta_hide = {
        "_cffi_ref",
        "_constraints",
        "_nursery",
        "_shapes",
        "_space",
        "_joints",
        "_position_func_cp",
        "_position_func_base",
        "_velocity_func_cp",
        "_velocity_func_base",
        "shapes",
        "constraints",
        "is_sleeping",
    }
    _init_kwargs = {
        *_pickle_args,
        *_pickle_kwargs[2:],
        "space",
        "name",
        "radians",
        "omega",
    }
    # Default values for rarely used attributes
    _position_func_base: Optional[PositionFuncT] = None  # For pickle
    _velocity_func_base: Optional[VelocityFuncT] = None  # For pickle
    _position_func_cp: Any = None  # For pickle
    _velocity_func_cp: Any = None  # For pickle

    _name: str = None
    _connected_bodies: Set["Body"]
    _connected_bodies = sk.lazy(lambda self: set())  # type: ignore
    color: Any = None
    description: str = None

    # Class constants
    _id_counter = 1

    #
    # Properties and static methods
    #
    @staticmethod
    def update_velocity(
        body: "Body", gravity: VecLike, damping: float, dt: float
    ) -> None:
        """Default rigid body velocity integration function.

        Updates the velocity of the body using Euler integration.
        """
        lib.cpBodyUpdateVelocity(body._cffi_ref, gravity, damping, dt)

    @staticmethod
    def update_position(body: "Body", dt: float) -> None:
        """Default rigid body position integration function.

        Updates the position of the body using Euler integration. Unlike the
        velocity function, it's unlikely you'll want to override this
        function. If you do, make sure you understand it's source code
        (in Chipmunk) as it's an important part of the collision/joint
        correction process.
        """
        lib.cpBodyUpdatePosition(body._cffi_ref, dt)

    @classmethod
    def _extract_options(cls, kwargs):
        """
        Extract init keyword args mutating dictionary and return those values.
        """
        opts = {}
        for k in cls._init_kwargs:
            if k in kwargs:
                opts[k] = kwargs.pop(k)
        return opts

    mass = cp_property[float]("cpBody(Get|Set)Mass", doc="Mass of the body")
    moment = cp_property[float](
        api="cpBody(Get|Set)Moment",
        doc="""Moment of inertia (MoI or sometimes just moment) of the body.
    
        The moment is like the rotational mass of a body.
        """,
    )
    position = cpvec_property(
        api="cpBody(Get|Set)Position",
        doc="""Position of the body.
    
        When changing the position you may also want to call
        :py:func:`Space.reindex_shapes_for_body` to update the collision 
        detection information for the attached shapes if plan to make any 
        queries against the space.""",
    )
    center_of_gravity = cpvec_property(
        "cpBody(Get|Set)CenterOfGravity",
        doc="""Location of the center of gravity in body local coordinates.
    
        The default value is (0, 0), meaning the center of gravity is the
        same as the position of the body.
        """,
    )
    velocity = cpvec_property(
        "cpBody(Get|Set)Velocity",
        doc="""Linear velocity of the center of gravity of the body.""",
    )
    force = cpvec_property(  # type: ignore
        "cpBody(Get|Set)Force",
        doc="""Force applied to the center of gravity of the body.
    
        This value is reset for every time step. Note that this is not the 
        total of forces acting on the body (such as from collisions), but the 
        force applied manually from the apply force functions.""",
    )
    angle = cp_property[float](
        api="cpBody(Get|Set)Angle",
        wrap=to_degrees,
        prepare=to_radians,
        doc="""Rotation of the body in degrees.
    
        When changing the rotation you may also want to call
        :py:func:`Space.reindex_shapes_for_body` to update the collision 
        detection information for the attached shapes if plan to make any 
        queries against the space. A body rotates around its center of gravity, 
        not its position.

        .. Note::
            If you get small/no changes to the angle when for example a
            ball is "rolling" down a slope it might be because the Circle shape
            attached to the body or the slope shape does not have any friction
            set.""",
    )
    radians = cp_property[float](
        api="cpBody(Get|Set)Angle", doc="""Rotation of the body in radians."""
    )
    angular_velocity = cp_property[float](
        api="cpBody(Get|Set)AngularVelocity",
        wrap=to_degrees,
        prepare=to_radians,
        doc="""The angular velocity of the body in degrees per second.""",
    )
    omega = cp_property[float](
        api="cpBody(Get|Set)AngularVelocity",
        doc="""The angular velocity of the body in radians per second.""",
    )
    torque = cp_property[float](
        api="cpBody(Get|Set)Torque",
        doc="""The torque applied to the body.

        This value is reset for every time step.""",
    )
    rotation_vector = cpvec_property(
        api="cpBody(Get)Rotation",
        doc="""The rotation vector for the body.""",
    )
    velocity_func: Callable[["Body", Vec2d, float, float], None]
    velocity_func = property(  # type: ignore
        lambda self: self._velocity_func_base,
        lambda self, fn: void(self._set_velocity_func(fn)),
        doc="""The velocity callback function. 
        
        The velocity callback function is called each time step, and can be 
        used to set a body's velocity.

            ``func(body : Body, gravity, damping, dt)``

        There are many cases when this can be useful. One example is individual 
        gravity for some bodies, and another is to limit the velocity which is 
        useful to prevent tunneling. 
        
        Example of a callback that limits the velocity:

        >>> body = mk.Body(1, 2)
        >>> max_velocity = 1000
        >>> def limit_velocity(body, gravity, damping, dt):
        ...     mk.Body.update_velocity(body, gravity, damping, dt)
        ...     speed = body.velocity.length
        ...     if speed > max_velocity:
        ...         body.velocity *= (max_velocity / speed)
        ...
        >>> body.velocity_func = limit_velocity
        """,
    )
    position_func: Callable[["Body", float], None]
    position_func = property(  # type: ignore
        lambda self: self._position_func_base,
        lambda self, fn: void(self._set_position_func(fn)),
        doc="""The position callback function. 
            
        The position callback function is called each time step and can be 
        used to update the body's position.

            ``func(body, dt) -> None``
        """,
    )

    @property
    def body_type(self) -> BodyType:
        """The type of a body (:py:const:`Body.DYNAMIC`,
        :py:const:`Body.KINEMATIC` or :py:const:`Body.STATIC`).

        When changing an body to a dynamic body, the mass and moment of
        inertia are recalculated from the shapes added to the body. Custom
        calculated moments of inertia are not preserved when changing types.
        This function cannot be called directly in a collision callback.

        This function accepts strings.

        >>> body = Body(mass=1)
        >>> body.body_type = "static"
        >>> body.mass
        inf
        """
        with lock_space(self):
            return lib.cpBodyGetType(self._cffi_ref)

    @body_type.setter
    def body_type(self, value: BodyType):
        kind = BODY_TYPES.get(value, value)
        lib.cpBodySetType(self._cffi_ref, kind)

    @property
    def is_sleeping(self) -> bool:
        """Returns true if the body is sleeping."""
        return bool(lib.cpBodyIsSleeping(self._cffi_ref))

    @property
    def space(self) -> Optional["Space"]:
        """
        Get the :py:class:`Space` that the body has been added to (or None).
        """
        return self._space

    @property
    def constraints(self) -> Constraints:
        """Get the constraints this body is attached to.

        The body only keeps a weak reference to the constraints and a
        live body wont prevent GC of the attached constraints"""
        return Constraints(self, self._iter_constraints)

    @property
    def shapes(self) -> Shapes:
        """Get the shapes attached to this body.

        The body only keeps a weak reference to the shapes and a live
        body wont prevent GC of the attached shapes"""
        return Shapes(self, self._shapes.__iter__)

    @property
    def arbiters(self) -> Set["Arbiter"]:
        """
        Return list of arbiters on this body.

        Arbiters in this set are "frozen" and can be used only for introspection.
        If you want to affect the state of collisions, use the :meth:`each_arbiter`
        method.
        """
        res: Set["Arbiter"] = set()
        self.each_arbiter(lambda arb: res.add(arb.properties))
        return res

    #
    # Physical quantities
    #
    @property
    def kinetic_energy(self) -> float:
        """
        Kinetic energy for angular and linear components.
        """
        # TODO: use ffi method?
        v2 = self.velocity.dot(self.velocity)
        w2 = self.angular_velocity * self.angular_velocity
        return 0.5 * (
            (self.mass * v2 if v2 else 0.0) + (self.moment * w2 if w2 else 0.0)
        )

    @property
    def gravitational_energy(self) -> float:
        """
        Potential energy due to gravity. Zero if not included in a space.

        Examples:
            >>> sp = Space(gravity=(0, -10))
            >>> body = sp.create_body(mass=2, position=(0, 10))
            >>> body.gravitational_energy
            200.0
        """
        if self.space is None:
            return 0.0
        gravity = self.space.gravity
        return -self.mass * self.position.dot(gravity)

    @property
    def linear_momentum(self) -> Vec2d:
        """
        Body's linear momentum (mass times velocity).

        Examples:
            >>> body = Body(mass=5, moment=10, velocity=(0, 10), angular_velocity=60)
            >>> body.linear_momentum
            Vec2d(0, 50)
        """
        return self.mass * self.velocity

    @property
    def angular_momentum(self) -> float:
        """
        Angular momentum around the center of mass.

        Examples:
            >>> body = Body(mass=5, moment=10, velocity=(0, 10), angular_velocity=60)
            >>> body.angular_momentum == approx(10 * 60 * (pi / 180))
            True
        """
        return self.moment * self.omega

    @property
    def density(self) -> float:
        """
        Overall density of body. If a density value is assigned, it fixes the
        density of all shapes in body.

        Examples:
            >>> body = PolyBody.new_box((3, 4), mass=6.0)
            >>> body.density
            0.5
            >>> body.density = 1.0; body.mass
            12.0
        """
        if self.body_type != self.DYNAMIC:
            return float("inf")

        mass = 0.0
        area = 0.0
        for s in self._shapes:
            mass += s.mass
            area += s.area
        return (self.mass or mass) / area

    @density.setter
    def density(self, value):
        self.shapes.apply(density=value)
        if self.body_type == self.DYNAMIC:
            self.mass = value * sum(s.area for s in self._shapes)

    @property
    def elasticity(self) -> Optional[float]:
        """
        Get/Set elasticity of shapes connected to body.

        Elasticity is None if body has not connected shapes or if shapes have
        different elasticities.
        """
        try:
            value, *other = set(s.elasticity for s in self._shapes)
        except IndexError:
            return None
        else:
            return None if other else value

    @elasticity.setter
    def elasticity(self, value):
        self.shapes.apply(elasticity=value)

    @property
    def friction(self) -> Optional[float]:
        """
        Get/Set friction of shapes connected to body.

        friction is None if body has not connected shapes or if shapes have
        different friction coefficients.
        """
        try:
            value, *other = {s.friction for s in self._shapes}
        except IndexError:
            return None
        else:
            return None if other else value

    @friction.setter
    def friction(self, value):
        self.shapes.apply(friction=value)

    @property
    def name(self):
        """
        Unique name for body in space.

        This is a read-only property set during body's creation. You cannot
        add two bodies with the same name to space.
        """
        return self._name

    @property
    def _id(self) -> int:
        """
        Unique id of the Body

        .. note::
            Experimental API. Likely to change in future major, minor or point
            releases.
        """
        return int(ffi.cast("int", lib.cpBodyGetUserData(self._cffi_ref)))

    @property
    def _safe_space(self) -> "Space":
        """
        A reference to space, but raises ValueError if space is None.
        """
        if self._space is None:
            raise ValueError("body must be connected to a space")
        return self._space

    def __init__(
        self,
        mass: float = 0,
        moment: float = 0,
        body_type: BodyType = DYNAMIC,
        *,
        space=None,
        name=None,
        **kwargs,
    ) -> None:
        body_type = BODY_TYPES.get(body_type, body_type)

        # Important checks that prevent segfaults
        if body_type == Body.DYNAMIC:
            if not isfinite(mass) or mass < 0:
                raise ValueError(f"invalid mass: {mass}")
            if isnan(moment) or moment < 0:
                raise ValueError(f"invalid moment: {moment}")

        if body_type == Body.DYNAMIC:
            self._cffi_ref = ffi.gc(lib.cpBodyNew(mass, moment), cffi_free_body)
        elif body_type == Body.KINEMATIC:
            self._cffi_ref = ffi.gc(lib.cpBodyNewKinematic(), cffi_free_body)
        elif body_type == Body.STATIC:
            self._cffi_ref = ffi.gc(lib.cpBodyNewStatic(), cffi_free_body)
        else:
            raise ValueError(f"invalid body type: {body_type!r}")

        self._space: Optional["Space"] = None
        self._shapes: Set["Shape"] = set()

        CREATED_BODIES[self._set_id()] = self
        init_attributes(self, self._init_kwargs, kwargs)

        if name is not None:
            self._name = name
        if space is not None:
            space.add(self)

    def __getstate__(self):
        args, meta = super().__getstate__()

        if self._position_func_cp is not None:
            meta["position_func"] = self._position_func_base
        if self._velocity_func_cp is not None:
            meta["velocity_func"] = self._velocity_func_base

        meta["$shapes"] = {s.copy(body=None) for s in list(self._shapes)}
        return args, meta

    def __setstate__(self, state):
        args, meta = state
        shapes = meta.pop("$shapes")
        super().__setstate__((args, meta))

        for shape in shapes:
            shape.body = self

    def __repr__(self) -> str:
        cls = type(self).__name__
        if self.name:
            return f"{cls}(name=%r)" % self.name
        elif self.body_type == Body.DYNAMIC:
            return f'{cls}(%r, %r, "dynamic")' % (self.mass, self.moment)
        elif self.body_type == Body.KINEMATIC:
            return f'{cls}(body_type="kinematic")'
        else:
            return f'{cls}(body_type="static")'

    def _iter_bounding_boxes(self, cache) -> Iterator["BB"]:
        if cache:
            for s in self._shapes:
                if not s.sensor:
                    yield s.cache_bb()
        else:
            for s in self._shapes:
                if not s.sensor:
                    yield s.bb

    def _iter_joints(self):
        if (space := self._space) is None:
            return

        joints = space._junctions
        for other in self._connected_bodies:
            yield joints[sort_body_pair(self, other)]

    def _iter_constraints(self):
        for joint in self._iter_joints():
            yield from joint

    def _iter_shapes(self):
        yield from self._shapes

    def _iter_game_object_children(self):
        return self._iter_shapes()

    def _set_id(self) -> int:
        counter = Body._id_counter
        lib.cpBodySetUserData(self._cffi_ref, ffi.cast("cpDataPointer", counter))
        Body._id_counter += 1
        return counter

    def _create_shape(self, cls, args, kwargs):
        shape = cls(*args, **kwargs)
        self.add_shape(shape)
        return shape

    def add_shape(self: BodyT, shape: "Shape") -> BodyT:
        """
        Attach shape to body.
        """
        shape_ref = shape._cffi_ref
        body_ref = self._cffi_ref
        if lib.cpShapeGetBody(shape_ref) != body_ref:
            lib.cpShapeSetBody(shape_ref, body_ref)

        self._shapes.add(shape)
        if (space := self._space) is not None:
            space.run_safe(self._add_shape_to_space, shape)
        return self

    def _add_shape_to_space(self, shape: Shape) -> None:
        assert isinstance(shape, Shape)

        if (space := self._space) is not None:
            shape_ref = shape._cffi_ref
            space_ref = space._cffi_ref
            if not lib.cpSpaceContainsShape(space_ref, shape_ref):
                lib.cpSpaceAddShape(space_ref, shape_ref)
        shape._space = space

    def remove_shape(self: BodyT, shape: "Shape") -> BodyT:
        """
        Remove shape from body.
        """
        self._shapes.remove(shape)
        shape._body = None
        if shape._space is not None:
            self._space.run_safe(self._remove_shape_from_space, shape)
        return self

    def _remove_shape_from_space(self, shape: Shape) -> None:
        assert isinstance(shape, Shape)

        if (space := shape._space) is not None:
            shape_ref = shape._cffi_ref
            space_ref = space._cffi_ref
            if lib.cpSpaceContainsShape(space_ref, shape_ref):
                lib.cpSpaceRemoveShape(space_ref, shape_ref)
        shape._space = None

    def detach(self):
        """
        Detach object and all shapes, joints and constraints from space.
        """

        if (space := self._space) is None:
            return

        for shape in self._shapes:
            space.run_safe(self._remove_shape_from_space, shape)

        for joint in self._iter_joints():
            joint.detach()

        if (space := self._space) is not None:
            space.run_safe(self._remove_body_from_space, space)

        self._space = None

    def _remove_body_from_space(self, space: "Space") -> None:
        space_ref = space._cffi_ref
        body_ref = self._cffi_ref

        if lib.cpSpaceContainsBody(space_ref, body_ref):
            lib.cpSpaceRemoveBody(space_ref, body_ref)

        space._bodies.remove(self)
        if self.name is not None:
            del space._named_bodies[self.name]

    def _set_velocity_func(self, func: VelocityFuncT) -> None:
        @ffi.callback("cpBodyVelocityFunc")
        def _impl(_: ffi.CData, gravity: ffi.CData, damping: float, dt: float) -> None:
            func(self, Vec2d(gravity.x, gravity.y), damping, dt)

        self._velocity_func_base = func
        self._velocity_func_cp = _impl
        lib.cpBodySetVelocityUpdateFunc(self._cffi_ref, _impl)

    def _set_position_func(self, func: Callable[["Body", float], None]) -> None:
        @ffi.callback("cpBodyPositionFunc")
        def _impl(_: ffi.CData, dt: float) -> None:
            return func(self, dt)

        self._position_func_base = func
        self._position_func_cp = _impl
        lib.cpBodySetPositionUpdateFunc(self._cffi_ref, _impl)

    def copy(self: BodyT, **kwargs) -> BodyT:
        f"""{CpCFFIBase.copy.__doc__}"""
        new = cast(BodyT, super().copy(**kwargs))
        for shape in self._shapes:
            sp = shape.copy(body=new)
            new._nursery.append(sp)
        return new

    def step(self, dt: float):
        """
        Evolve body applying forces.
        """
        self.apply_impulse_at_local_point(self.force * dt, self.center_of_gravity)
        self.force *= 0

        self.apply_angular_impulse(self.torque * dt)
        self.torque *= 0

        if self._space is None:
            gravity = getattr(self._space, "gravity", Vec2d.zero())
            damping = ...
        else:
            gravity = (0, 0)
            damping = 1.0

        self.velocity_func(self, gravity, damping, dt)
        self.position_func(self, dt)
        return self

    def cache_bb(self):
        for s in self._shapes:
            s.cache_bb()
        return self.bb

    def activate(self: BodyT) -> BodyT:
        """Reset the idle timer on a body.

        If it was sleeping, wake it and any other bodies it was touching.
        """
        lib.cpBodyActivate(self._cffi_ref)
        return self

    def sleep(self: BodyT) -> BodyT:
        """Forces a body to fall asleep immediately even if it's in midair.

        Cannot be called from a callback.
        """
        if self._space is None:
            raise Exception("Body not added to space")
        lib.cpBodySleep(self._cffi_ref)
        return self

    def sleep_with_group(self: BodyT, body: "Body") -> BodyT:
        """Force a body to fall asleep immediately along with other bodies
        in a group.

        When objects in Pymunk sleep, they sleep as a group of all objects
        that are touching or jointed together. When an object is woken up,
        all of the objects in its group are woken up.
        :py:func:`Body.sleep_with_group` allows you group sleeping objects
        together. It acts identically to :py:func:`Body.sleep` if you pass
        None as group by starting a new group. If you pass a sleeping body
        for group, body will be awoken when group is awoken. You can use this
        to initialize levels and start stacks of objects in a pre-sleeping
        state.
        """
        if self._space is None:
            raise Exception("Body not added to space")
        lib.cpBodySleepWithGroup(self._cffi_ref, body._cffi_ref)
        return self

    #
    # Manage collisions
    #
    def each_arbiter(
        self: BodyT, func: Callable[..., Any] = set_attrs, /, *args: Any, **kwargs: Any
    ) -> BodyT:
        """Run func on each of the arbiters on this body.

            ``func(arbiter, *args, **kwargs) -> None``

            Callback Parameters
                arbiter : :py:class:`Arbiter`
                    The Arbiter
                args
                    Optional parameters passed to the callback function.
                kwargs
                    Optional keyword parameters passed on to the callback function.

        The default function is :py:func:`set_attrs` and simply set attributes
        passed as keyword parameters.

        .. warning::

            Do not hold on to the Arbiter after the callback!
        """

        @ffi.callback("cpBodyArbiterIteratorFunc")
        def cf(_body, arb, _) -> None:
            if self._space is None:
                raise ValueError("Body does not belong to any space")
            arbiter = Arbiter(arb, self._space)
            func(arbiter, *args, **kwargs)
            arbiter.close()

        with lock_space(self):
            lib.cpBodyEachArbiter(self._cffi_ref, cf, ffi.new_handle(self))
        return self

    #
    # Manage shapes
    #
    def reindex_shapes(self: BodyT) -> BodyT:
        """
        Reindex all shapes in body.

        It is a NO-OP if body is not in a space.
        """
        space = self.space
        if space is not None:
            space.reindex_shapes_for_body(self)
        return self

    def clear_shapes(self: BodyT) -> BodyT:
        """
        Remove all shapes from object.

        If body is bound to space, shapes are also removed from space.
        """
        while self._shapes:
            shape = self._shapes.pop()
            self._remove_shape_from_space(shape)
        return self

    #
    # Forces and impulses
    #
    def apply_force(self: BodyT, force: VecLike) -> BodyT:
        """
        Apply force to the center of mass (does not produce any resulting torque).
        """
        self.force += force
        return self

    def apply_torque(self: BodyT, torque: float) -> BodyT:
        """
        Apply toque to the center of mass (does not produce any resulting force).
        """
        self.torque += torque
        return self

    def apply_force_at_world_point(
        self: BodyT, force: VecLike, point: VecLike
    ) -> BodyT:
        """Add the force force to body as if applied from the world point.

        People are sometimes confused by the difference between a force and
        an impulse. An impulse is a very large force applied over a very
        short period of time. Some examples are a ball hitting a wall or
        cannon firing. Chipmunk treats impulses as if they occur
        instantaneously by adding directly to the velocity of an object.
        Both impulses and forces are affected the mass of an object. Doubling
        the mass of the object will halve the effect.
        """
        lib.cpBodyApplyForceAtWorldPoint(self._cffi_ref, force, point)
        return self

    def apply_force_at_local_point(
        self: BodyT, force: VecLike, point: VecLike = (0, 0)
    ) -> BodyT:
        """
        Add the local force force to body as if applied from the body
        local point.
        """
        lib.cpBodyApplyForceAtLocalPoint(self._cffi_ref, force, point)
        return self

    def apply_impulse(self: BodyT, impulse: VecLike) -> BodyT:
        """
        Add the impulse to body without changing angular components.
        """
        self.velocity += Vec2d.from_coords(impulse) / self.mass
        return self

    def apply_angular_impulse(self: BodyT, impulse: float) -> BodyT:
        """
        Add the angular impulse to body without changing linear velocities.
        """
        self.omega += impulse / self.moment
        return self

    def apply_impulse_at_world_point(
        self: BodyT, impulse: VecLike, point: VecLike
    ) -> BodyT:
        """
        Add the impulse impulse to body as if applied from the world point.
        """
        lib.cpBodyApplyImpulseAtWorldPoint(self._cffi_ref, impulse, point)
        return self

    def apply_impulse_at_local_point(
        self: BodyT, impulse: VecLike, point: VecLike = (0, 0)
    ) -> BodyT:
        """Add the local impulse impulse to body as if applied from the body
        local point.
        """
        lib.cpBodyApplyImpulseAtLocalPoint(self._cffi_ref, impulse, point)
        return self

    #
    # Conversion between system of coordinates
    #
    def local_to_world(self, v: VecLike) -> Vec2d:
        """Convert body local coordinates to world space coordinates

        Many things are defined in coordinates local to a body meaning that
        the (0,0) is at the center of gravity of the body and the axis rotate
        along with the body.

        Args:
            v: Vector in body local coordinates
        """
        u = lib.cpBodyLocalToWorld(self._cffi_ref, v)
        return Vec2d(u.x, u.y)

    def world_to_local(self, v: VecLike) -> Vec2d:
        """Convert world space coordinates to body local coordinates

        Args:
            v: Vector in world space coordinates
        """
        u = lib.cpBodyWorldToLocal(self._cffi_ref, v)
        return Vec2d(u.x, u.y)

    def local_to_local(self, v: VecLike, other: "Body") -> Vec2d:
        """
        Convert local coordinates in self to local coordinates in other.

        Args:
            v: Vector in body local coordinates
            other: target body. Convert to local coordinates of that body.
        """
        u1 = lib.cpBodyLocalToWorld(self._cffi_ref, v)
        u2 = lib.cpBodyWorldToLocal(other._cffi_ref, u1)
        return Vec2d(u2.x, u2.y)

    def velocity_at_world_point(self, point: VecLike) -> Vec2d:
        """Get the absolute velocity of the rigid body at the given world
        point

        It's often useful to know the absolute velocity of a point on the
        surface of a body since the angular velocity affects everything
        except the center of gravity.
        """
        v = lib.cpBodyGetVelocityAtWorldPoint(self._cffi_ref, point)
        return Vec2d(v.x, v.y)

    def velocity_at_local_point(self, point: VecLike) -> Vec2d:
        """Get the absolute velocity of the rigid body at the given body
        local point
        """
        v = lib.cpBodyGetVelocityAtLocalPoint(self._cffi_ref, point)
        return Vec2d(v.x, v.y)

    #
    # Transforms
    #
    def rotate(self: BodyT, angle: float, axis: AxisT = None) -> BodyT:
        """
        Rotate body by angle.

        Args:
            angle: angle in degrees.
            axis: axis of rotation.
        """
        if axis is not None:
            center = normalize_axis(self, axis)
            self.position += center.rotated(angle) - center
        self.angle += angle
        return self

    def rotate_radians(self: BodyT, radians: float, axis: AxisT = None):
        """
        Like :meth:`rotate`, but uses radians.
        """
        return self.rotate(degrees(radians), axis)

    @overload
    def move(self: BodyT, /, x: float, y: float) -> BodyT:
        ...

    @overload
    def move(self: BodyT, /, vec: VecLike) -> BodyT:
        ...

    def move(self, *args):
        """
        Move body by displacement. Can be given as a single vector argument or
        two (x, y) coordinates.
        """
        self.position += args[0] if len(args) == 1 else args
        return self

    @overload
    def boost(self: BodyT, /, x: float, y: float) -> BodyT:
        ...

    @overload
    def boost(self: BodyT, /, vec: VecLike) -> BodyT:
        ...

    def boost(self, *args):
        """
        Boost speed by the given displacement. Can be given as a single vector
        argument or two (vx, vy) coordinates.
        """
        self.velocity += args[0] if len(args) == 1 else args
        return self

    def angular_boost(self: BodyT, angular_velocity: float) -> BodyT:
        """
        Boost angular velocity by the given amount.
        """
        self.angular_velocity += angular_velocity
        return self

    def omega_boost(self: BodyT, omega: float) -> BodyT:
        """
        Boost angular velocity by the given amount in radians/sec.
        """
        self.omega += omega
        return self

    def fuse_with(self: BodyT, other: "Body") -> BodyT:
        """
        Fuse with a copy of all shapes of other object into self.
        """
        from .shapes import Circle, Poly

        for shape in other._shapes:
            if isinstance(shape, Circle):
                offset = self.world_to_local(other.local_to_world(shape.offset))
                shape = Circle(shape.radius, offset, self)
            elif isinstance(shape, Poly):
                vertices = [
                    self.world_to_local(v) for v in shape.get_vertices(world=True)
                ]
                shape = Poly(vertices, radius=shape.radius, body=self)
            else:
                raise NotImplementedError

            if self.space is not None:
                self.space.add(shape)
            else:
                self._nursery.append(shape)

        self.mass += other.mass
        self.moment += other.moment  # FIXME: that is not how moments work ;)
        return self

    def _mirror(self, value) -> Tuple[Vec2d, Vec2d]:
        if value == "left":
            bb = self.cache_bb()
            return Vec2d(bb.left, 0), Vec2d(1, 0)
        raise NotImplementedError

    def _flip(self: BodyT, axis) -> BodyT:
        from .shapes import Circle, Poly

        p0, n = self._mirror(axis)
        t = n.perpendicular()

        def pt_transform(p: Vec2d):
            d = p - p0
            return p0 + d - 2 * t * p.dot(t)

        for shape in self._shapes:
            if isinstance(shape, Circle):
                shape.offset = pt_transform(shape.offset)
            elif isinstance(shape, Poly):
                vertices = [pt_transform(v) for v in shape.get_vertices()]
                shape.set_vertices(vertices)
            else:
                raise NotImplementedError

        return self

    def scale(
        self: BodyT, scale: float, axis: AxisT = None, physics: bool = False
    ) -> BodyT:
        """
        Transform all shapes in object by the given scale factor.

        Args:
            scale:
                Scale factor.
            axis:
                Reference point to apply scale transformation.
            physics:
                If True, also apply transformation to physical properties.
                In a 2D-world, mass increases with the square of scaling and
                moments with the fourth power.
        """
        from .shapes import Circle, Poly

        if axis is not None:
            raise NotImplementedError

        transform = Transform.scaling(scale)
        for shape in self._shapes:
            if isinstance(shape, Circle):
                shape.radius *= scale
                shape.offset = transform(shape.offset)
            elif isinstance(shape, Poly):
                vertices = [transform(v) for v in shape.get_vertices()]
                shape.set_vertices(vertices)
            elif isinstance(shape, Segment):
                shape.endpoints = transform(shape.a), transform(shape.b)
            else:
                raise NotImplementedError(type(shape), Segment)
        self.reindex_shapes()

        if physics:
            self.mass *= scale ** 2
            self.moment *= scale ** 4

        return self

    #
    # Constraints
    #
    def pin_position(
        self: BodyT,
        target: VecLike = None,
        *,
        anchor: VecLike = None,
        world: bool = False,
        **kwargs,
    ) -> PositionJoint:
        f"""
        Pin object at target point.

        Args:
            target:
                Target point to pin body to. Uses local coordinates if
                world=False (default) and world coordinates otherwise.
            anchor:
                Usually the anchor point is the same as target and the constraint
                will always work to satisfy this condition. It will apply
                (possibly unbounded) forces to drive the object back to the
                position in which anchor point coincides with the target point.

                Anchor point is always given in local coordinates.
            world:
                If true, target point is given in world coordinates. If the
                anchor point is given, it is **not** affected by this option.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        kwargs["world"] = world

        if anchor is None:
            args = () if target is None else (target,)
            return self.junction().pivot(*args, **kwargs)

        args = (anchor,) if target is None else (anchor, target)
        return self.junction().pivot(*args, **kwargs)

    def pin_distance(
        self,
        target: VecLike,
        *args,
        tol: Union[None, float, VecLike] = None,
        anchor: VecLike = Vec2d.zero(),
        world: bool = False,
        **kwargs,
    ) -> Union[DistanceJoint, LimitDistanceJoint]:
        f"""
        Keep distance of object to target point (in local coordinates) fixed.

        Args:
            joint.pin_distance(target):
                Keeps the current distance to target.
            joint.fix_distance(target, distance):
                Keeps the given distance between anchor points.
            joint.fix_distance(target, min, max):
                Keeps distance to target within bounds. There is
                no problem in setting min=0.0 and max=float('inf').

        Keyword Args:
            tol:
                If given, defines a tolerance of acceptable separation
                distances. Can be given as a number or a tuple of (tol_left,
                tol_right).
            world:
                If True, target point is given in world coordinates.
            anchor:
                Anchor point in body. It is always given in local coordinates,
                even if world = True.
            {CONSTRAINT_KWARGS_DOC}
        """
        if not world:
            target = self.local_to_world(target)
        kwargs["anchor_a"] = anchor
        kwargs["anchor_b"] = target
        return self.junction().fix_distance(*args, tol=tol, **kwargs)

    def fix_angle(self, *args, **kwargs) -> LimitAngleJoint:
        f"""
        Constrain angle of object in the range (a, b).

        Receive between zero and two positional arguments.

        * **body.fix_angle()**
          Keeps the current angle.
        * **body.fix_angle(angle)**
          Force angle to value.
        * **body.fix_angle(min, max)**
          Limit angle in range. The range can be greater than a full rotation.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        return self.junction().fix_angle(*args, **kwargs)

    def fix_radians(self, *args, **kwargs) -> LimitAngleJoint:
        """
        Constrain angle of object.

        Like :meth:`fix_angle`, but angles are given in radians.
        """
        return self.junction().fix_radians(*args, **kwargs)

    def fix_angular_velocity(
        self, rate: float = None, **kwargs
    ) -> AngularVelocityJoint:
        f"""
        Constrain angular velocity to a given value in degrees/sec.

        If no value is given, uses the current velocity.

        This constraint is the basis for building simple motors.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        rate = self.angular_velocity if rate is None else rate
        return self.junction().fix_angular_velocity(rate, **kwargs)

    def fix_omega(self, rate: float = 0.0, **kwargs) -> AngularVelocityJoint:
        """
        Constrain angular velocity.

        Like :meth:`fix_angular_velocity` but accept rate in radians/sec.
        """
        rate = self.omega if rate is None else rate
        return self.junction().fix_omega(rate, **kwargs)

    def motor(self, rate: float = 0.0, **kwargs):
        """
        An alias to meth:`fix_angular_velocity`.
        """
        return self.fix_angular_velocity(rate, **kwargs)

    def motor_radians(self, rate: float = 0.0, **kwargs):
        """
        An alias to meth:`fix_omega`.
        """
        return self.fix_omega(rate, **kwargs)

    def prevent_clockwise_rotations(self, ratchet=1, **kwargs) -> RatchetJoint:
        f"""
        Prevent object from rotating in the clockwise direction.

        This works by creating a RatchetJoint with the world's static body.
        It accepts the default set of constraint keyword arguments.

        Args:
            ratchet:
                Size of ratchet in degrees. In special circumstances, body may
                rotate in both directions within a tolerance between two ratchet
                "clicks".
        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        return self.junction().ratchet(-ratchet, **kwargs)

    def prevent_counterclockwise_rotations(self, ratchet=1, **kwargs) -> RatchetJoint:
        """
        Prevent object from rotating in the counterclockwise direction.

        Accept the same arguments as :meth:`prevent_clockwise_rotations`.
        """
        return self.junction().ratchet(+ratchet, **kwargs)

    def spring_to(
        self,
        target: VecLike,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_length: float = None,
        *,
        anchor: VecLike = (0, 0),
        world: bool = False,
        **kwargs,
    ) -> DampedSpring:
        f"""
        Connect body to target point (in local coordinates) with a spring.

        Args:
            target:
                Target point to fix spring in local coordinates.
            stiffness:
                The spring constant (Young's modulus).
            damping:
                How soft to make the damping of the spring.
            rest_length:
                Rest length o string. If not given or None, consider the initial
                distance.
            world:
                If True, target refers to world coordinates.
            anchor:
                Anchor point in object. Always given in local coordinates, even
                if world=True.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        if not world:
            target = self.local_to_world(target)
        args = stiffness, damping, rest_length, anchor, target
        return self.junction().spring(*args, **kwargs)

    def rotary_spring(
        self,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_angle: float = None,
        **kwargs,
    ) -> DampedRotarySpring:
        f"""
        Fix angle with a rotary spring.

        Args:
            stiffness:
                The spring constant (Young's modulus).
            damping:
                How soft to make the damping of the spring.
            rest_angle:
                Angle the body want to have. Keep current angle, if not given.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        args = stiffness, damping, rest_angle
        return self.junction().rotary_spring(*args, **kwargs)

    def rotary_spring_radians(
        self,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_angle: float = None,
        **kwargs,
    ) -> DampedRotarySpring:
        """
        Fix angle with a rotary spring.

        Like :meth:`rotary_spring`, but angles are given in radians.
        """
        args = stiffness, damping, rest_angle
        return self.junction().rotary_spring_radians(*args, **kwargs)

    def pin_to_segment(
        self,
        start: VecLike,
        end: VecLike,
        anchor: VecLike = None,
        *,
        world: bool = False,
        inner: bool = False,
        ratio: float = None,
        **kwargs: ConstraintKwargs,
    ) -> SegmentJoint:
        f"""
        Pin object at a linear slider from point start to end points (in local
        coordinates).

        Args:
            start:
                Start of segment slider.
            end:
                Start of segment slider.
            anchor:
                Anchor point in body.
            ratio:
                If given in place of an anchor, select anchor point by choosing
                a point in segment. The point is choosing by interpolating
                start and end with the given ratio.
            inner:
                If True, attach the world anchor point to a inner slider
                from start to end in body.
            world:
                If True, start, end and anchor are given in world coordinates.
        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        if inner:
            return self._pin_to_inner_segment(
                start, end, anchor, ratio, world, **kwargs
            )

        if anchor is not None and world:
            anchor = self.world_to_local(anchor)
        if not world:
            start = self.local_to_world(start)
            end = self.local_to_world(end)

        kwargs["ratio"] = ratio
        return self.junction().fix_to_segment(start, end, anchor, flip=True, **kwargs)

    def _pin_to_inner_segment(self, start, end, anchor, ratio, world, **kwargs):
        if anchor is not None and not world:
            anchor = self.local_to_world(anchor)
        if world:
            start = self.world_to_local(start)
            end = self.world_to_local(end)
        kwargs["ratio"] = ratio
        return self.junction().fix_to_segment(start, end, anchor, flip=False, **kwargs)

    def junction(self, other: "Body" = None) -> Junction:
        """
        Create joint between two bodies.

        A joint is used to add constraints between two bodies.
        """
        if other is None:
            other = self._safe_space.static_body

        return self._safe_space.junction(self, other)

    #
    # Interfaces
    #

    # Game object interface
    def draw(self, camera=None, shapes=None):
        camera = get_drawing_options(camera)
        shapes = self.shapes if shapes is None else shapes
        for shape in shapes:
            shape.draw(camera)

    # Describe
    def _describe_body(self, indent, memo) -> List[str]:
        if self.description:
            yield ""
        yield indent + "# PROPERTIES"
        yield from super()._describe_body(indent, memo)

        yield ""
        yield indent + "# SHAPES"
        for i, s in enumerate(self.shapes, 1):
            for ln in s.describe(name=f"[{i}]", memo=memo).splitlines():
                yield indent + ln


class StaticBody(Body):
    """
    An static body.

    It cannot change speed, position, body type, and others. Main use is to
    serve as the default static_body of a space.
    """

    position = property(Body.position.__get__)  # type: ignore
    velocity = property(Body.velocity.__get__)  # type: ignore
    angle = property(Body.angle.__get__)  # type: ignore
    radians = property(Body.radians.__get__)  # type: ignore
    angular_velocity = property(Body.angular_velocity.__get__)  # type: ignore
    omega = property(Body.omega.__get__)  # type: ignore
    body_type = property(Body.body_type.__get__)  # type: ignore
    mass: float = float("inf")  # type: ignore
    moment: float = float("inf")  # type: ignore

    def __init__(self):
        super().__init__(body_type=Body.STATIC)


#
# Specialized bodies
#
class BodyShape(Body):
    """
    Base class for bodies with a single shape.
    """

    shape: "Shape"

    # Properties
    radius: float = sk.delegate_to("shape", mutable=True)
    area: float = sk.delegate_to("shape")
    collision_type: int = sk.delegate_to("shape", mutable=True)
    filter: "ShapeFilter" = sk.delegate_to("shape", mutable=True)
    elasticity: float = sk.delegate_to("shape", mutable=True)
    friction: float = sk.delegate_to("shape", mutable=True)
    surface_velocity: Vec2d = sk.delegate_to("shape", mutable=True)
    bb: "BB" = sk.delegate_to("shape")
    center: Vec2d = sk.delegate_to("shape")
    center_world: Vec2d = sk.delegate_to("shape")

    # Methods
    point_query = sk.delegate_to("shape")
    segment_query = sk.delegate_to("shape")
    shapes_collide = sk.delegate_to("shape")
    radius_of_gyration_sqr = sk.delegate_to("shape")

    @property
    def body(self: BodyT) -> BodyT:
        return self

    def _post_init(self):
        if self.body_type != Body.DYNAMIC:
            return

        if self.mass == 0:
            shape = self.shape
            if self.space:
                shape.density = 1.0
            else:
                density = shape.density or 1.0
                self.mass = density * shape.area
                self.moment = self.mass * shape.radius_of_gyration_sqr()
        elif self.moment == 0:
            self.moment = float("inf")


class CircleBody(BodyShape, Body):
    """
    A body attached to a single circular shape.
    """

    offset: Vec2d = sk.delegate_to("shape", mutable=True)
    offset_world: Vec2d = sk.delegate_to("shape", mutable=True)

    def __init__(self, radius, offset=(0, 0), **kwargs):
        opts = self._extract_options(kwargs)
        super().__init__(**opts)
        self.shape: "Circle" = Circle(radius, offset, body=self, **kwargs)
        self._post_init()


class SegmentBody(BodyShape, Body):
    """
    A body attached to a single circular shape.
    """

    a: Vec2d = sk.delegate_to("shape", mutable=True)
    a_world: Vec2d = sk.delegate_to("shape", mutable=True)
    b: Vec2d = sk.delegate_to("shape", mutable=True)
    b_world: Vec2d = sk.delegate_to("shape", mutable=True)
    endpoints: Tuple[Vec2d, Vec2d] = sk.delegate_to("shape", mutable=True)
    endpoints_world: Tuple[Vec2d, Vec2d] = sk.delegate_to("shape", mutable=True)

    def __init__(self, a, b, radius=0, **kwargs):
        if "position" in kwargs:
            cm = Vec2d.from_coords(kwargs["position"])
            super().__init__(**self._extract_options(kwargs))
            self.shape: "Segment" = Segment(a - cm, b - cm, radius, self, **kwargs)
        else:
            offset = kwargs.pop("offset", (0, 0))
            kwargs["position"] = cm = (Vec2d.from_coords(a) + b) * 0.5 - offset
            super().__init__(**self._extract_options(kwargs))
            self.shape: "Segment" = Segment(a - cm, b - cm, radius, self, **kwargs)
        self._post_init()


class PolyBody(BodyShape, Body):
    """
    A body attached to a single polygonal shape.
    """

    vertices: List[Vec2d] = sk.delegate_to("shape", mutable=True)
    vertices_world: List[Vec2d] = sk.delegate_to("shape", mutable=True)
    get_vertices = sk.delegate_to("shape")
    set_vertices = sk.delegate_to("shape")

    @classmethod
    def _new_from_shape_factory(cls, mk_shape, *args, **kwargs):
        new = object.__new__(PolyBody)
        Body.__init__(new, **new._extract_options(kwargs))
        new.shape = mk_shape(new, *args, **kwargs)
        new._post_init()
        return new

    @classmethod
    def new_box(cls, size: VecLike = (10, 10), radius: float = 0.0, **kwargs):
        mk_box = lambda body, *args, **opts: Poly.new_box(size, radius, body, **opts)
        return cls._new_from_shape_factory(mk_box, **kwargs)

    @classmethod
    def new_box_bb(cls, bb: "BB", radius: float = 0.0, **kwargs):
        mk_box = lambda body, **opts: Poly.new_box_bb(bb, radius, body, **opts)
        return cls._new_from_shape_factory(mk_box, **kwargs)

    @classmethod
    def new_regular_poly(
        cls,
        n: int,
        size: float,
        radius: float = 0.0,
        *,
        angle: float = 0.0,
        offset: VecLike = (0, 0),
        **kwargs,
    ):
        mk_box = lambda body, **opts: Poly.new_regular_poly(
            n, size, radius, body, angle=angle, offset=offset, **opts
        )
        return cls._new_from_shape_factory(mk_box, **kwargs)

    def __init__(self, vertices, radius=0, transform=None, offset=None, **kwargs):
        if "position" not in kwargs:
            kwargs["position"] = center = centroid(vertices)
            if center != (0, 0):
                vertices = [v - center for v in vertices]
        super().__init__(**self._extract_options(kwargs))
        self.shape: "Poly" = Poly(vertices, radius, self, transform, offset, **kwargs)
        self._post_init()


#
# Utility functions
#
def cffi_free_body(cp_body):
    logging.debug("bodyfree start %s", cp_body)
    cp_shapes = []
    cp_constraints = []

    @ffi.callback("cpBodyShapeIteratorFunc")
    def cf1(_, shape, __):
        cp_shapes.append(shape)

    @ffi.callback("cpBodyConstraintIteratorFunc")
    def cf2(_, constraint, __):
        cp_constraints.append(constraint)

    lib.cpBodyEachShape(cp_body, cf1, ffi.NULL)
    for cp_shape in cp_shapes:
        logging.debug("free %s %s", cp_body, cp_shape)
        cp_space = lib.cpShapeGetSpace(cp_shape)
        if cp_space != ffi.NULL:
            lib.cpSpaceRemoveShape(cp_space, cp_shape)

    lib.cpBodyEachConstraint(cp_body, cf2, ffi.NULL)
    for cp_constraint in cp_constraints:
        logging.debug("free %s %s", cp_body, cp_constraint)
        cp_space = lib.cpConstraintGetSpace(cp_constraint)
        if cp_space != ffi.NULL:
            lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)

    cp_space = lib.cpBodyGetSpace(cp_body)
    if cp_space != ffi.NULL:
        lib.cpSpaceRemoveBody(cp_space, cp_body)

    logging.debug("bodyfree free %s", cp_body)
    lib.cpBodyFree(cp_body)


def normalize_axis(body: Body, obj: AxisT) -> Vec2d:
    """
    Return axis from string.
    """
    if obj == "middle":
        return body.cache_bb().center() - body.position
    elif obj == "pos":
        return Vec2d(0.0, 0.0)
    return Vec2d.from_coords(obj)


@contextmanager
def lock_space(body: Body):
    """
    Lock space inside context manager.
    """
    if body.space is None:
        yield
    else:
        with body.space.locked():
            yield


@overload
def body_from_cffi(ptr: None) -> None:
    ...


@overload
def body_from_cffi(ptr: ffi.CData) -> Body:
    ...


def body_from_cffi(ptr):
    """
    Internal function that returns shape from cffi pointer.
    """
    if not bool(ptr):
        return None

    id_ = int(ffi.cast("int", lib.cpBodyGetUserData(ptr)))
    try:
        return CREATED_BODIES[id_]
    except KeyError:
        raise ValueError("Shape does not exist")


def sort_body_pair(a: Body, b: Body) -> Tuple[Body, Body]:
    """
    Sort body pair so the firstly created body always appear first.
    """
    assert isinstance(a, Body)
    assert isinstance(b, Body)
    return (b, a) if a._id > b._id else (a, b)
