"""
A constraint is something that describes how two bodies interact with
each other. (how they constrain each other). Constraints can be simple
joints that allow bodies to pivot around each other like the bones in your
body, or they can be more abstract like the gear joint or motors.

This submodule contain all the constraints that are supported by Pymunk.

All the constraints support copy and pickle from the standard library. Custom 
properties set on a constraint will also be copied/pickled.

Chipmunk has a good overview of the different constraint on youtube which
works fine to showcase them in Pymunk as well.
http://www.youtube.com/watch?v=ZgJJZTS0aMM

.. raw:: html

    <iframe width="420" height="315" style="display: block; margin: 0 auto;"
    src="http://www.youtube.com/embed/ZgJJZTS0aMM" frameborder="0"
    allowfullscreen></iframe>

"""
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    TypeVar,
    TypedDict,
    Tuple,
    Union,
)
from ..cp import ffi, lib, cp_property, cpvec_property
from ..abc import CpCFFIBase, GameObjectInterface
from ..linalg.math import radians as to_radians, degrees as to_degrees, pi
from ..util import void, cffi_body, init_attributes
from ..linalg import Vec2d
from ..typing import VecLike

if TYPE_CHECKING:
    from .body import Body
    from .space import Space
    from .junction import Junction

RangeLimit = Union[float, type(...)]
Range = Tuple[RangeLimit, RangeLimit]
SolveFunc = Callable[["Constraint"], None]
ForceFunc = Callable[[float], float]
T = TypeVar("T")
C = TypeVar("C")

REST_ANGLE = "The relative angle in radians that the bodies want to have"
DAMPING = "How soft to make the damping of the spring."
ANCHOR_A = "Anchor point in local coordinates of body A."
ANCHOR_B = "Anchor point in local coordinates of body B."
DEG = dict(wrap=to_degrees, prepare=to_radians)
INVDEG = dict(prepare=to_degrees, wrap=to_radians)


class ConstraintOpts(TypedDict, total=False):
    """
    max_force:
        The maximum force that the constraint can use to act on the two
        bodies.

        Defaults to infinity.
    error_bias:
        The percentage of joint error that remains unfixed after a
        second.
    max_bias:
        The maximum speed at which the constraint can apply error correction.
    collide_bodies:
        False to prevent collisions between the two bodies in the constraint.
    pre_solve:
        A function called before the constraint solver runs.
    post_solve:
        A function called after the constraint solver runs.
    """

    max_force: float
    error_bias: float
    max_bias: float
    collide_bodies: bool
    pre_solve: SolveFunc
    post_solve: SolveFunc


# Waiting for some resolution of: https://github.com/python/mypy/issues/4441
# ConstraintKwargs = "Expand[ConstraintOpts]"
ConstraintKwargs = Any


class Constraint(GameObjectInterface, CpCFFIBase):
    """Base class of all constraints.

    You usually don't want to create instances of this class directly, but
    instead use one of the specific constraints such as the PinJoint.
    """

    is_constraint = True
    _pickle_args = ["a", "b"]
    _pickle_kwargs = ["max_force", "error_bias", "max_bias", "collide_bodies"]
    _pickle_meta_hide = {
        "_a",
        "_b",
        "_cffi_ref",
        "_cffi_backend",
        "_nursery",
        "_cp_post_solve_func",
        "_cp_pre_solve_func",
        "_post_solve_func",
        "_pre_solve_func",
    }
    _init_kwargs = {*_pickle_args, *_pickle_kwargs, "pre_solve", "post_solve"}
    _pre_solve_func: Optional[SolveFunc] = None
    _post_solve_func: Optional[SolveFunc] = None
    _cp_pre_solve_func: Any = ffi.NULL
    _cp_post_solve_func: Any = ffi.NULL

    max_force = cp_property[float](
        "cpConstraint(Get|Set)MaxForce",
        doc="""The maximum force that the constraint can use to act on the two
        bodies.
        """,
    )
    error_bias = cp_property[float](
        "cpConstraint(Get|Set)ErrorBias",
        doc="""The percentage of joint error that remains unfixed after a
        second.

        This works exactly the same as the collision bias property of a space,
        but applies to fixing error (stretching) of joints instead of
        overlapping collisions.

        Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of
        the error every 1/60th of a second.
        """,
    )
    max_bias = cp_property[float](
        "cpConstraint(Get|Set)MaxBias",
        doc="""The maximum speed at which the constraint can apply error
        correction.

        Defaults to infinity
        """,
    )
    collide_bodies = cp_property[bool](
        "cpConstraint(Get|Set)CollideBodies",
        wrap=bool,
        doc="""Constraints can be used for filtering collisions too.

        When two bodies collide, Easymunk ignores the collisions if this property
        is set to False on any constraint that connects the two bodies.
        Defaults to True. This can be used to create a chain that self
        collides, but adjacent links in the chain do not collide.
        """,
    )

    @property
    def impulse(self) -> float:
        """
        The most recent impulse that constraint applied to bodies.

        To convert this to a force, divide by the time step passed to
        space.step(). You can use this to implement breakable joints to check
        if the force they attempted to apply exceeded a certain threshold.
        """
        return lib.cpConstraintGetImpulse(self._cffi_ref)

    @property
    def a(self) -> "Body":
        """The first of the two bodies constrained"""
        return self._a

    @property
    def b(self) -> "Body":
        """The second of the two bodies constrained"""
        return self._b

    @property
    def pre_solve(self) -> Optional[SolveFunc]:
        """The pre-solve function is called before the constraint solver runs.

        Note that None can be used to reset it to default value.
        """
        return self._pre_solve_func

    @pre_solve.setter
    def pre_solve(self, func: Optional[SolveFunc]):
        self._pre_solve_func = func

        if func is not None:

            @ffi.callback("cpConstraintPreSolveFunc")
            def _impl(_constraint, _space) -> None:
                if self.a.space is None:
                    raise ValueError("body a is not attached to any space")
                fn(self)

            fn = func
            self._cp_pre_solve_func = _impl
        else:
            self._cp_pre_solve_func = ffi.NULL

        lib.cpConstraintSetPreSolveFunc(self._cffi_ref, self._cp_pre_solve_func)

    @property
    def post_solve(self) -> Optional[SolveFunc]:
        """The post-solve function is called after the constraint solver runs.

        Note that None can be used to reset it to default value.
        """
        return self._post_solve_func

    @post_solve.setter
    def post_solve(self, func: Optional[SolveFunc]) -> None:
        self._post_solve_func = func
        if func is not None:

            @ffi.callback("cpConstraintPostSolveFunc")
            def _impl(_constraint, _space) -> None:
                if self.a.space is None:
                    raise ValueError("body a is not attached to any space")
                fn(self)

            fn = func
            self._cp_post_solve_func = _impl
        else:
            self._cp_post_solve_func = ffi.NULL

        lib.cpConstraintSetPostSolveFunc(self._cffi_ref, self._cp_post_solve_func)

    @property
    def space(self) -> Optional["Space"]:
        return self._space

    @property
    def junction(self) -> Optional["Junction"]:
        return self._junction

    def __init__(
        self, a: "Body", b: "Body", _constraint: Any, **kwargs: ConstraintKwargs
    ) -> None:
        if a is b:
            raise ValueError("cannot apply constraint to same body")

        self._cffi_ref = ffi.gc(_constraint, cffi_free_constraint)
        self._a = a
        self._b = b
        self._space = None
        self._junction = None
        init_attributes(self, self._init_kwargs, kwargs)

    def __getstate__(self):
        args, meta = super().__getstate__()
        if hasattr(self, "_pre_solve_func"):
            meta["pre_solve"] = self.pre_solve
        if hasattr(self, "_post_solve_func"):
            meta["post_solve"] = self.post_solve
        return args, meta

    def _iter_game_object_children(self):
        # Bodies are not children of constraints to avoid
        # double iteration over bodies.
        yield from ()

    def activate_bodies(self) -> None:
        """Activate the bodies this constraint is attached to"""
        self._a.activate()
        self._b.activate()

    def detach(self) -> None:
        """
        Detach itself from joints group and space.
        """
        if self._junction is not None:
            self._junction.remove_constraint(self)
        else:
            self._space = None

    def step(self, dt):
        # TODO: update at least one iteration of constraint solver?
        return self


class AbstractDistanceJoint(Constraint):
    """
    Base class for SlideJoint, PinJoint and Pivot joint.

    Each of those constraints are special cases of the previous one. We unify
    all of them in a common API and sub-class hierarchy.
    """

    anchor_a: Vec2d
    anchor_b: Vec2d
    min_distance: float
    max_distance: float
    distance: float
    distance_vector: Vec2d


class LimitDistanceJoint(AbstractDistanceJoint):
    """
    Keep distance between anchor points within bounds.

    A chain could be modeled using this joint. It keeps the anchor points
    from getting to far apart, but will allow them to get closer together.

    Args:

    Arguments a and b are the two bodies to connect, anchor_a and anchor_b are
    the anchor points on those bodies, and min and max define the allowed
    distances of the anchor points.

    """

    _pickle_args = [
        *Constraint._pickle_args,
        "min_distance",
        "max_distance",
        "anchor_a",
        "anchor_b",
    ]
    anchor_a = cpvec_property("cpSlideJoint(Get|Set)AnchorA", doc=ANCHOR_A)
    anchor_b = cpvec_property("cpSlideJoint(Get|Set)AnchorB", doc=ANCHOR_B)
    min_distance = cp_property[float](
        "cpSlideJoint(Get|Set)Min", doc="Minimum distance between anchor points."
    )
    max_distance = cp_property[float](
        "cpSlideJoint(Get|Set)Max", doc="Maximum distance between anchor points."
    )

    @property
    def distance_vector(self) -> Vec2d:
        """
        Distance vector between two anchor points.
        """
        return self._a.local_to_local(self.anchor_a, self._b) - self.anchor_b

    @property
    def distance(self) -> float:
        """
        Distance between objects. Clamped to the [min, max] range.
        """
        size = self.distance_vector.length
        return max(min(size, self.max), self.min)

    @distance.setter
    def distance(self, value: float):
        self.min = value
        self.max = value

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        a: "Body",
        b: "Body",
        min: RangeLimit = 0.0,
        max: RangeLimit = float("inf"),
        anchor_a: VecLike = (0, 0),
        anchor_b: VecLike = (0, 0),
        **kwargs: ConstraintKwargs,
    ):
        ref_a = cffi_body(a)
        ref_b = cffi_body(b)
        if anchor_a is None and anchor_b is None:
            raise ValueError("Cannot determine anchor point if both anchors are None")
        elif anchor_a is None:
            anchor_a = b.local_to_local(anchor_b, a)
        elif anchor_b is None:
            anchor_b = a.local_to_local(anchor_a, b)
        if min is ...:
            min = 0.0
        if max is ...:
            max = float("inf")
        ptr = lib.cpSlideJointNew(ref_a, ref_b, anchor_a, anchor_b, min, max)
        super().__init__(a, b, ptr, **kwargs)


class DistanceJoint(AbstractDistanceJoint):
    """
    Keeps the anchor points at a set distance from one another.

    Distance joints are an specific case of a DistanceLimitJoint with
    joint.min_distance = joint.max_distance = joint.distance.

    Arguments a and b are the two bodies to connect, and anchor_a and anchor_b
    are the anchor points on those bodies.

    The distance between the two anchor points is measured when the joint
    is created. If you want to set a specific distance, use the setter
    function to override it.
    """

    _pickle_args = [*Constraint._pickle_args, "distance", "anchor_a", "anchor_b"]
    anchor_a = cpvec_property("cpPinJoint(Get|Set)AnchorA", doc=ANCHOR_A)
    anchor_b = cpvec_property("cpPinJoint(Get|Set)AnchorB", doc=ANCHOR_B)
    distance: float
    distance = property(  # type: ignore
        lambda self: lib.cpPinJointGetDist(self._cffi_ref),
        lambda self, distance: void(lib.cpPinJointSetDist(self._cffi_ref, distance)),
        doc="""Fixed distance between anchor points.""",
    )

    # Properties of slide joints.
    distance_vector = LimitDistanceJoint.distance_vector
    min_distance = property(lambda self: self.distance)
    max_distance = property(lambda self: self.distance)

    def __init__(
        self,
        a: "Body",
        b: "Body",
        distance: float = None,
        anchor_a: VecLike = (0, 0),
        anchor_b: VecLike = (0, 0),
        **kwargs: ConstraintKwargs,
    ):
        ptr = lib.cpPinJointNew(cffi_body(a), cffi_body(b), anchor_a, anchor_b)
        super().__init__(a, b, ptr, **kwargs)
        if distance is not None:
            self.distance = distance


class PositionJoint(AbstractDistanceJoint):
    """
    Keep anchor points at the same position.

    Because the pivot location is given in world coordinates, you must
    have the bodies moved into the correct positions already.
    Alternatively you can specify the joint based on a pair of anchor
    points, but make sure you have the bodies in the right place as the
    joint will fix itself as soon as you start simulating the space.

    That is, either create the joint with PositionJoint(a, b, pivot) or
    PositionJoint(a, b, anchor_a, anchor_b).

    Args:
        a: The first of the two bodies
        b: The second of the two bodies
        *args: Either one pivot point, or two anchor points

    Note:
        Position joints are equivalent to DistanceJoints with distance = 0 or
        SegmentJoints with segment_start = segment_end = anchor.
    """

    _pickle_args = [*Constraint._pickle_args, "anchor_a", "anchor_b"]
    anchor_a = cpvec_property("cpPivotJoint(Get|Set)AnchorA", doc=ANCHOR_A)
    anchor_b = cpvec_property("cpPivotJoint(Get|Set)AnchorB", doc=ANCHOR_B)
    groove_a = property(lambda self: self.anchor_a)
    groove_b = property(lambda self: self.anchor_a)

    # Properties of slide joints.
    distance_vector = property(lambda self: Vec2d.zero())
    distance = property(lambda self: 0.0)
    min_distance = property(lambda self: 0.0)
    max_distance = property(lambda self: 0.0)

    def __init__(
        self,
        a: "Body",
        b: "Body",
        *args: VecLike,
        **kwargs: ConstraintKwargs,
    ):
        ref_a = cffi_body(a)
        ref_b = cffi_body(b)
        if (n := len(args)) == 1:
            ptr = lib.cpPivotJointNew(ref_a, ref_b, args[0])
        elif n == 2:
            ptr = lib.cpPivotJointNew2(ref_a, ref_b, args[0], args[1])
        else:
            msg = "You must specify either one pivot point" " or two anchor points"
            raise TypeError(msg)
        super().__init__(a, b, ptr, **kwargs)


class SegmentJoint(Constraint):
    """
    Fix anchor point on body B to segment on body A. The anchor point can slide
    freely inside the line segment.

    All coordinates are body local.

    Args:
        a: The first of the two bodies
        b: The second of the two bodies
        segment_start: Start of segment relative to body A.
        segment_end: Start of segment relative to body B.
        anchor: Anchor point in body B.
    """

    _pickle_args = [
        *Constraint._pickle_args,
        "segment_start",
        "segment_end",
        "anchor",
    ]

    anchor = cpvec_property("cpGrooveJoint(Get|Set)AnchorB")
    segment_start = cpvec_property("cpGrooveJoint(Get|Set)GrooveA")
    segment_end = cpvec_property("cpGrooveJoint(Get|Set)GrooveB")

    def __init__(
        self,
        a: "Body",
        b: "Body",
        segment_start: VecLike,
        segment_end: VecLike,
        anchor: VecLike = (0, 0),
        **kwargs: ConstraintKwargs,
    ):
        _constraint = lib.cpGrooveJointNew(
            cffi_body(a), cffi_body(b), segment_start, segment_end, anchor
        )
        super().__init__(a, b, _constraint, **kwargs)


class DampedSpring(Constraint):
    """Connect objects with a spring.

    The spring allows you to define the rest length, stiffness and damping.

    Args:
        a:
            The first of the two bodies
        b:
            The second of the two bodies
        stiffness:
            The spring constant (Young's modulus). This constant is measured
            in [force] / [distance] (N/m, in SI units). The higher the value,
            the stiffer the spring. It can be zero or even negative (which
            produces diverging springs).
        damping:
            How soft to make the damping of the spring. It has units of
            [mass] / [time] (kg/s, in SI units) and contributes with a force
            F = -damping * v.
        rest_length:
            Equilibrium distance for the spring.
        anchor_a:
            First anchor point, relative to body A.
        anchor_b:
            Second anchor point, relative to body B.
    """

    _pickle_args = [
        *Constraint._pickle_args,
        "stiffness",
        "damping",
        "rest_length",
        "anchor_a",
        "anchor_b",
    ]
    _pickle_meta_hide = [*Constraint._pickle_meta_hide, "_cp_force_func", "_force_func"]
    _init_kwargs = {*Constraint._init_kwargs, "force_func"}
    _cp_force_func: Any = ffi.NULL

    anchor_a = cpvec_property("cpDampedSpring(Get|Set)AnchorA")
    anchor_b = cpvec_property("cpDampedSpring(Get|Set)AnchorB")
    rest_length = cp_property[float]("cpDampedSpring(Get|Set)RestLength")
    stiffness = cp_property[float]("cpDampedSpring(Get|Set)Stiffness")
    damping = cp_property[float]("cpDampedSpring(Get|Set)Damping")

    @property
    def force_func(self):
        return self._force_func

    @force_func.setter
    def force_func(self, fn: ForceFunc):
        self._force_func = fn  # type: ignore

        @ffi.callback("cpDampedSpringForceFunc")
        def force_func(_, dist: float) -> float:
            return fn(dist)

        self._cp_force_func = force_func
        lib.cpDampedSpringSetSpringForceFunc(self._cffi_ref, force_func)

    def __init__(
        self,
        a: "Body",
        b: "Body",
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_length: float = None,
        anchor_a: VecLike = (0, 0),
        anchor_b: VecLike = (0, 0),
        **kwargs: ConstraintKwargs,
    ):

        if rest_length is None:
            rest_length = (anchor_a - b.local_to_local(anchor_b, a)).length

        ptr = lib.cpDampedSpringNew(
            cffi_body(a),
            cffi_body(b),
            anchor_a,
            anchor_b,
            rest_length,
            stiffness,
            damping,
        )
        super().__init__(a, b, ptr, **kwargs)

    def __getstate__(self):
        args, meta = super().__getstate__()
        if hasattr(self, "_force_func"):
            meta["force_func"] = self.force_func
        return args, meta

    def _force_func(self, dist):
        """Default force function"""
        return -self.stiffness * (dist - self.rest_length)


class DampedRotarySpring(Constraint):
    """
    DampedRotarySpring works like the DampedSpring but in a angular fashion.

    Like a damped spring, but works in an angular fashion.

    Args:
        a:
            The first of the two bodies.
        b:
            The second of the two bodies.
        stiffness:
            The spring constant (Young's modulus). This constant gives the
            proportionality between torque and the angular displacement. It
            is measured in [torque] / [angle] (Nm/rad, in SI units). The higher
            the value, the stiffer the spring. It can be zero or even negative (which
            produces diverging springs). It contributes with a torque of
            tau = -stiffness * relative_angle.
        damping:
            How soft to make the damping of the spring. It has units of
            [moment of inertia] / time (kg m^2/s, in SI units) and contributes
            with a torque of tau = -damping * angular_velocity.
        rest_angle:
            The relative angle in radians that the bodies want to have. Keep
            current angle, if not given.
        radians:
            If True, rest angle is given in radians. Stiffness and damping are
            also reinterpreted to produce a torque of
            tau = -stiffness * relative_radians - damping * omega.
    """

    _pickle_args = [
        *Constraint._pickle_args,
        "stiffness",
        "damping",
        "rest_angle",
    ]
    _init_kwargs = {*Constraint._init_kwargs, "torque_func"}
    _cp_torque_func: Any = ffi.NULL

    rest_angle = cp_property[float]("cpDampedRotarySpring(Get|Set)RestAngle", **DEG)
    stiffness = cp_property[float]("cpDampedRotarySpring(Get|Set)Stiffness", **INVDEG)
    damping = cp_property[float]("cpDampedRotarySpring(Get|Set)Damping", **INVDEG)

    rest_radians = cp_property[float]("cpDampedRotarySpring(Get|Set)RestAngle")
    stiffness_radians = cp_property[float]("cpDampedRotarySpring(Get|Set)Stiffness")
    damping_radians = cp_property[float]("cpDampedRotarySpring(Get|Set)Damping")

    @property
    def torque_func(self):
        return self._torque_func

    @torque_func.setter
    def torque_func(self, fn: ForceFunc):
        self._torque_func = fn  # type: ignore

        @ffi.callback("cpDampedSpringForceFunc")
        def torque_func(_, radians: float) -> float:
            return fn(to_degrees(radians))

        self._cp_torque_func = torque_func
        lib.cpDampedRotarySpringSetSpringTorqueFunc(self._cffi_ref, torque_func)

    def __init__(
        self,
        a: "Body",
        b: "Body",
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_angle: float = None,
        radians=False,
        **kwargs: ConstraintKwargs,
    ):

        if rest_angle is None:
            angle = b.radians - a.radians
        elif not radians:
            angle = to_radians(rest_angle)
        else:
            angle = rest_angle

        if not radians:
            stiffness *= 180 / pi
            damping *= 180 / pi

        ptr = lib.cpDampedRotarySpringNew(
            cffi_body(a), cffi_body(b), angle, stiffness, damping
        )
        super().__init__(a, b, ptr, **kwargs)

    def __getstate__(self):
        args, meta = super().__getstate__()
        if hasattr(self, "_torque_func"):
            meta["torque_func"] = self.torque_func
        return args, meta

    def _torque_func(self, angle):
        """Default force function"""
        return self.stiffness * (angle - self.rest_angle)


class LimitAngleJoint(Constraint):
    """
    Constrains the relative angle between two bodies.

    It is implemented so that it's possible to for the range to be greater than
    a full revolution.
    """

    _pickle_args = [*Constraint._pickle_args, "min_angle", "max_angle"]

    min_angle = cp_property[float]("cpRotaryLimitJoint(Get|Set)Min", **DEG)
    max_angle = cp_property[float]("cpRotaryLimitJoint(Get|Set)Max", **DEG)

    min_radians = cp_property[float]("cpRotaryLimitJoint(Get|Set)Min")
    max_radians = cp_property[float]("cpRotaryLimitJoint(Get|Set)Max")

    @property
    def angle(self):
        return to_degrees((self.min_radians + self.max_radians) / 2)

    @angle.setter
    def angle(self, value):
        self.min_radians = self.max_radians = to_radians(value)

    @property
    def radians(self):
        return (self.min_radians + self.max_radians) / 2

    @radians.setter
    def radians(self, value):
        self.min_radians = self.max_radians = value

    def __init__(
        self,
        a: "Body",
        b: "Body",
        min: float = None,
        max: float = None,
        radians=False,
        **kwargs: ConstraintKwargs,
    ):
        if min is None:
            min = a.radians - b.radians
        elif not radians:
            min = to_radians(min)

        if max is None:
            max = min
        elif not radians:
            max = to_radians(max)

        ref_a = cffi_body(a)
        ref_b = cffi_body(b)
        ptr = lib.cpRotaryLimitJointNew(ref_a, ref_b, min, max)
        super().__init__(a, b, ptr, **kwargs)


class RatchetJoint(Constraint):
    """
    Works like a socket wrench.

    Ratchet is the distance between "clicks", phase is the initial offset
    to use when deciding where the ratchet angles are.
    """

    _pickle_args = [*Constraint._pickle_args, "ratchet", "phase"]

    angle = cp_property[float]("cpRatchetJoint(Get|Set)Angle", **DEG)
    phase = cp_property[float]("cpRatchetJoint(Get|Set)Phase", **DEG)
    ratchet = cp_property[float]("cpRatchetJoint(Get|Set)Ratchet", **DEG)

    radians = cp_property[float]("cpRatchetJoint(Get|Set)Angle")
    phase_radians = cp_property[float]("cpRatchetJoint(Get|Set)Phase")
    ratchet_radians = cp_property[float]("cpRatchetJoint(Get|Set)Ratchet")

    def __init__(
        self,
        a: "Body",
        b: "Body",
        ratchet: float = 1.0,
        phase: float = None,
        radians=False,
        **kwargs: ConstraintKwargs,
    ):
        if not radians:
            if phase is not None:
                phase = to_radians(phase)
            ratchet = to_radians(ratchet)

        ref_a = cffi_body(a)
        ref_b = cffi_body(b)
        ptr = lib.cpRatchetJointNew(ref_a, ref_b, phase or 0.0, ratchet)
        super().__init__(a, b, ptr, **kwargs)

        if phase is None:
            self.phase_radians = self.radians

    def click(self):
        """
        Control the phase to make the
        """
        self.radians = self.phase_radians


class AngularRatioJoint(Constraint):
    """
    Keeps the ratio between angles of two bodies constant.

    This joint can be used to implement gear mechanisms.

    The constraint imposes that `ratio = a.angular_velocity / b.angular_velocity`

    Ratio is always measured in absolute terms. Phase is the initial angular
    offset of the two bodies.
    """

    _pickle_args = [*Constraint._pickle_args, "ratio", "phase"]

    ratio = cp_property[float]("cpGearJoint(Get|Set)Ratio")
    phase = cp_property[float]("cpGearJoint(Get|Set)Phase", **DEG)
    phase_radians = cp_property[float]("cpGearJoint(Get|Set)Phase")

    def __init__(
        self,
        a: "Body",
        b: "Body",
        ratio: float = 1.0,
        phase: float = None,
        radians=False,
        **kwargs: ConstraintKwargs,
    ):
        if phase is None:
            phase = b.radians * ratio - a.radians
        elif not radians:
            phase = to_radians(phase)
        ptr = lib.cpGearJointNew(cffi_body(a), cffi_body(b), phase, ratio)
        super().__init__(a, b, ptr, **kwargs)


class AngularVelocityJoint(Constraint):
    """
    Keeps the relative angular velocity constant.

    Used to implement simple motors.

    Args:
        rate:
            The desired relative angular velocity. You will usually want
            to set an force (torque) maximum for motors as otherwise they will be
            able to apply a nearly infinite torque to keep the bodies moving.
    """

    _pickle_args = [*Constraint._pickle_args, "rate"]

    rate = cp_property[float]("cpSimpleMotor(Get|Set)Rate", **DEG)
    rate_radians = cp_property[float]("cpSimpleMotor(Get|Set)Rate")

    def __init__(
        self,
        a: "Body",
        b: "Body",
        rate: float = 0.0,
        radians=False,
        **kwargs: ConstraintKwargs,
    ):
        if not radians:
            rate = to_radians(rate)
        ptr = lib.cpSimpleMotorNew(cffi_body(a), cffi_body(b), rate)
        super().__init__(a, b, ptr, **kwargs)

    def coast(self):
        """
        Disable motor by setting max_force = 0.
        """
        self.max_force = 0.0
        return self


def cffi_free_constraint(cp_constraint) -> None:
    cp_space = lib.cpConstraintGetSpace(cp_constraint)
    if cp_space != ffi.NULL:
        lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)

    logging.debug("free %s", cp_constraint)
    lib.cpConstraintFree(cp_constraint)
