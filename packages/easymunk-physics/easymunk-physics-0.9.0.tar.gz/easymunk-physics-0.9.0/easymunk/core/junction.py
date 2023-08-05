import weakref
from typing import Optional, TYPE_CHECKING, Union, Sequence, TypeVar, Callable

import sidekick.api as sk

from .constraints import (
    PositionJoint,
    DampedSpring,
    DampedRotarySpring,
    AngularVelocityJoint,
    DistanceJoint,
    LimitDistanceJoint,
    LimitAngleJoint,
    RatchetJoint,
    AngularRatioJoint,
    ConstraintKwargs,
    ConstraintOpts,
    Constraint,
    RangeLimit,
    SegmentJoint,
)
from ..abc import GameObjectInterface
from ..cp import lib
from ..linalg import Vec2d
from ..typing import VecLike

if TYPE_CHECKING:
    from .space import Space
    from .body import Body

J = TypeVar("J")
T = TypeVar("T")

CONSTRAINT_KWARGS_DOC = ConstraintOpts.__doc__
ANCHOR_DOCS = """
            anchor_a: Anchor point in object a
            anchor_b: Anchor point in object b
"""


class Junction(GameObjectInterface, Sequence[Constraint]):
    """
    An object that is used to control all constraints between a pair of objects.
    """

    a: "Body" = sk.alias("_a")
    b: "Body" = sk.alias("_b")
    space: "Space" = sk.alias("_space")

    @property
    def flipped(self) -> "Junction":
        """
        A copy of joint flipping body a for b.
        """
        try:
            flipped = self._flipped()
            if flipped is None:
                raise AttributeError
        except AttributeError:
            flipped = Junction(self._b, self._a, self._space)
            flipped._flipped = weakref.ref(self)
            flipped._constraints = self._constraints
            self._flipped = weakref.ref(flipped)
        return flipped

    @property
    def constraint(self) -> Optional["Constraint"]:
        """
        Last constraint created.
        """
        try:
            return self._constraints[-1]
        except IndexError:
            return None

    def __init__(self, a: "Body", b: "Body", space: "Space"):
        self._a = a
        self._b = b
        self._constraints = []
        self._space = space

    def __len__(self):
        return len(self._constraints)

    def __getitem__(self, idx):
        return self._constraints[idx]

    def __iter__(self):
        return iter(self._constraints)

    def _iter_game_object_children(self):
        return iter(self)

    #
    # Symmetric constraints
    #
    def pivot(
        self, *args, world: bool = False, **kwargs: ConstraintKwargs
    ) -> PositionJoint:
        f"""
        Create a pivot between both objects in the given local point.

        If a single point is given, that refers to the common anchor point in
        local coordinates.

        If two points are given, they refer to the anchor points in local
        coordinates. If those points do not coincide in world coordinates, the
        constraint may apply possibly unbound forces to connect them.

        Args:
            args:
                The anchor point in first body or a pair defining anchor points
                in each body. If no point is given, create an anchor point in the
                center of gravity of first body.
            world:
                If True, anchor points are given in world coordinates.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        if (n := len(args)) == 0:
            args = (self.a.local_to_world(self.a.center_of_gravity),)
        elif n == 1:
            if not world:
                args = (self.a.local_to_world(args[0]),)
        elif n == 2:
            if world:
                pt1, pt2 = args
                args = self.a.world_to_local(pt1), self.b.world_to_local(pt2)
        else:
            raise TypeError("expect at most 2 positional arguments")
        return self._create_constraint(PositionJoint, args, kwargs)

    def fix_distance(
        self,
        *args: RangeLimit,
        tol: float = None,
        anchor_a: VecLike = (0, 0),
        anchor_b: VecLike = (0, 0),
        world: bool = False,
        **kwargs: ConstraintKwargs,
    ) -> Union[DistanceJoint, LimitDistanceJoint]:
        f"""
        Keep two objects at a fixed distance between them.

        Receive between zero and two positional arguments.

        * **joint.fix_distance()**
          Keeps the current distance between anchor points.
        * **joint.fix_distance(distance)**
          Keeps the given distance between anchor points.
        * **joint.fix_distance(min, max)**
          Keeps distance between anchor points within bounds. There is no
          problem in setting min=0.0 and max=float('inf').

        Keyword Args:
            tol:
                If given, defines a tolerance of acceptable separation
                distances. Can be given as a number or a tuple of (tol_left,
                tol_right).
            world:
                If True, anchor points are given in world coordinates.
            {ANCHOR_DOCS}
            {CONSTRAINT_KWARGS_DOC}
        """

        # Convert anchor points to local coordinates
        if world:
            distance = Vec2d.from_displacement(anchor_a, anchor_b).length
            anchor_a = self.a.world_to_local(anchor_a)
            anchor_b = self.b.world_to_local(anchor_b)
        else:
            distance = (self.a.local_to_local(anchor_a, self.b) - anchor_b).length

        kwargs["anchor_a"] = anchor_a
        kwargs["anchor_b"] = anchor_b

        # Select the type of constraint and args
        if (n_args := len(args)) == 0:
            args = (distance,)
        elif n_args == 1:
            distance = args[0]
        elif n_args != 2:
            raise TypeError("function accepts 0 to 2 positional parameters")

        if tol is None:
            factory = LimitDistanceJoint if n_args == 2 else DistanceJoint
            return self._create_constraint(factory, args, kwargs)
        elif n_args == 2:
            raise ValueError("cannot specify tolerance with min and max distances")
        elif isinstance(tol, Sequence):
            tol_min, tol_max = tol
            args = (distance + tol_min, distance + tol_max)
        else:
            args = (distance - tol, distance + tol)

        return self._create_constraint(LimitDistanceJoint, args, kwargs)

    def fix_angle(self, *args, **kwargs: ConstraintKwargs) -> LimitAngleJoint:
        f"""
        Constrains the relative rotations of two bodies.

        Receive between zero and two positional arguments.

        * **joint.fix_angle()**
          Keeps the current angle between bodies.
        * **joint.fix_angle(angle)**
          Keeps the given relative angle between bodies.
        * **joint.fix_angle(min, max)**
          Limit relative angle in range. The range can be greater than
          a full rotation.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        return self._create_constraint(LimitAngleJoint, args, kwargs)

    def fix_radians(self: J, *args, **kwargs: ConstraintKwargs) -> LimitAngleJoint:
        """
        Constrains the relative rotations of two bodies.

        Like :meth:`fix_angle`, but angles are given in radians.
        """
        kwargs.setdefault("radians", True)
        return self._create_constraint(LimitAngleJoint, args, kwargs)

    def fix_angular_velocity(
        self, rate: float = 0.0, **kwargs: ConstraintKwargs
    ) -> AngularVelocityJoint:
        f"""
        Force a fixed relative angular velocity between two bodies.

        Useful for creating motors.

        Args:
            rate:
                Desired relative angular velocity in degrees/sec. Positive values
                induce counterclockwise rotations on body A and clockwise rotations
                on body B.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        return self._create_constraint(AngularVelocityJoint, (rate,), kwargs)

    def fix_omega(
        self: J, rate: float = 0.0, **kwargs: ConstraintKwargs
    ) -> AngularVelocityJoint:
        """
        Force a fixed relative angular velocity between two bodies.

        Like :meth:`fix_angular_velocity`, but uses angular velocity in
        radians/sec.
        """
        kwargs.setdefault("radians", True)
        return self._create_constraint(AngularVelocityJoint, (rate,), kwargs)

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

    def ratchet(
        self, ratchet: float = 1.0, phase: float = None, **kwargs: ConstraintKwargs
    ) -> RatchetJoint:
        f"""
        Keep angular positions of both objects synchronized by a wrench-like
        mechanism that allows rotation in one direction, but locks rotation in
        the other.

        For positive ratchet angles, a counterclockwise torque on body A is
        transmitted to body B, while a clockwise torque is not. The effect is
        flipped if torque is produced on B: a clockwise torque is transmitted to
        A, while a counterclockwise is not.

        This assumes the mathematical convention that positive y goes up. If
        the y coordinates are flipped (like the convention adopted by many
        computer graphics libraries), rotations are also flipped.

        The "ratchet" parameter is measured in angles and correspond to the
        tolerance in which angular positions are synchronized. In analogy with
        a wrench mechanism, this would be the angle between two "clicks".

        Args:
            ratchet:
                Angle between clicks in the ratchet mechanism. For small values,
                only the signal is of much importance. Positive angles transmit
                counterclockwise rotations from A to B and clockwise rotations
                from B to A. negative angles invert those rotations.

                A angle of zero disables the ratchet.
            phase:
                Position inside the ratchet. By the default selects a phase
                that starts ratchet in a "clicked" state.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        args = ratchet, phase
        return self._create_constraint(RatchetJoint, args, kwargs)

    def spring(
        self,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_length: Optional[float] = None,
        anchor_a: VecLike = (0, 0),
        anchor_b: VecLike = (0, 0),
        *,
        world=False,
        **kwargs: ConstraintKwargs,
    ) -> DampedSpring:
        f"""
        Connect two bodies with a spring.

        Args:
            stiffness:
                The spring constant (Young's modulus).
            damping:
                How soft to make the damping of the spring.
            rest_length:
                Rest length o string. If not given or None, consider the initial
                distance.
            anchor_a:
                Anchor point in body A.
            anchor_b:
                Anchor point in body B.
            world:
                If True, anchor points refers to world coordinates.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        if world:
            anchor_a = self.b.world_to_local(anchor_a)
            anchor_b = self.b.world_to_local(anchor_b)
        args = stiffness, damping, rest_length, anchor_a, anchor_b
        return self._create_constraint(DampedSpring, args, kwargs)

    def rotary_spring(
        self: J,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_angle: float = None,
        **kwargs: ConstraintKwargs,
    ) -> DampedRotarySpring:
        f"""
        Connect angular position of two bodies with a rotary spring.

        Args:
            stiffness:
                The spring constant (Young's modulus).
            damping:
                How soft to make the damping of the spring.
            rest_angle:
                The relative angle in radians that the bodies want to have. Keep
                current angle, if not given.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        args = stiffness, damping, rest_angle
        return self._create_constraint(DampedRotarySpring, args, kwargs)

    def rotary_spring_radians(
        self,
        stiffness: float = 0.0,
        damping: float = 0.0,
        rest_angle: float = None,
        **kwargs: ConstraintKwargs,
    ) -> DampedRotarySpring:
        """
        Connect angular position of two bodies with a rotary spring.

        Like :meth:`rotary_spring`, but angles are given in radians.
        """
        args = stiffness, damping, rest_angle
        kwargs.setdefault("radians", True)
        return self._create_constraint(DampedRotarySpring, args, kwargs)

    def fix_rotation_ratio(
        self: J, ratio: float = 1.0, phase: float = None, **kwargs: ConstraintKwargs
    ) -> AngularRatioJoint:
        f"""
        Force a fixed ratio between angular rotations of two bodies.

        Args:
            ratio:
                Ratio between desired a.angular_velocity / b.angular_velocity. A
                ratio of "m / n" means that every m rotations of a, produce n
                rotations of b.
            phase:
                Initial difference between rotations. The constraint imposes
                that ratio = (a.angle + phase) / b.angle

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        args = ratio, phase
        return self._create_constraint(AngularRatioJoint, args, kwargs)

    def fix_rotation_ratio_radians(
        self: J, ratio: float = 1.0, phase: float = None, **kwargs: ConstraintKwargs
    ) -> AngularRatioJoint:
        """
        Force a fixed ratio between angular rotations of two bodies.

        Like :meth:`fix_rotation_ratio`, but phase angle is given in radians.
        """
        args = ratio, phase
        kwargs.setdefault("radians", True)
        return self._create_constraint(AngularRatioJoint, args, kwargs)

    def gear(
        self, ratio: float = 1.0, phase: float = None, **kwargs: ConstraintKwargs
    ) -> AngularRatioJoint:
        """
        An alias to :meth:`fix_rotation_ratio`
        """
        return self.fix_rotation_ratio(ratio, phase, **kwargs)

    def gear_radians(
        self, ratio: float = 1.0, phase: float = None, **kwargs: ConstraintKwargs
    ) -> AngularRatioJoint:
        """
        An alias to :meth:`fix_rotation_ratio_radians`
        """
        return self.fix_rotation_ratio_radians(ratio, phase, **kwargs)

    #
    # Asymmetric constraints
    #
    def fix_to_segment(
        self,
        start: VecLike,
        end: VecLike,
        anchor: VecLike = None,
        *,
        flip: bool = False,
        ratio: float = None,
        **kwargs: ConstraintKwargs,
    ) -> SegmentJoint:
        f"""
        Attach body B to a segment from `start` to `end` in in body A.

        The anchor point in B is free to slide between the two ends of segment.

        Positions are specified in local body coordinates.

        Args:
            start:
                Start of segment slider in first body.
            end:
                Start of segment slider in first body.
            anchor:
                Anchor point in second body.
            ratio:
                If given in place of an anchor, select anchor point by choosing
                a point in segment. The point is choosing by interpolating
                start and end with the given ratio.
            flip:
                Flip the roles of A and B. If flip=True, segment is placed in
                body B which attaches to anchor point in body A.

        Keyword Args:
            {CONSTRAINT_KWARGS_DOC}
        """
        if flip:
            kwargs["ratio"] = ratio
            return self.flipped.fix_to_segment(start, end, anchor, **kwargs)

        if ratio is None and anchor is None:
            anchor = (0, 0)
        elif anchor is None:
            anchor = Vec2d.from_coords(start).interpolate_to(end, ratio)
            anchor = self.a.local_to_local(anchor, self.b)
        elif ratio is not None:
            raise TypeError("cannot specify ratio and anchor at the same time")

        args = start, end, anchor
        return self._create_constraint(SegmentJoint, args, kwargs)

    #
    # Auxiliary methods
    #
    def _create_constraint(
        self, cls: Callable[..., T], args, kwargs: ConstraintOpts
    ) -> T:
        cons = cls(self.a, self.b, *args, **kwargs)
        self.add_constraint(cons)
        return cons

    def detach(self: J) -> J:
        """
        Detach joint and constraints from space.
        """
        self.clear()
        self._space = None
        return self

    def destroy(self: J) -> J:
        """
        Destroy joint, making it unusable.
        """
        self.detach()
        self._a = self._b = self._constraints = None
        return self

    def clear(self: J) -> J:
        """
        Clear all constraints detaching them from space, but keeps the
        joint alive.
        """
        for constraint in reversed(self._constraints):
            self.remove_constraint(constraint)
        return self

    def add_constraint(self: J, constraint: Constraint) -> J:
        """
        Manually add constraint to list.

        The constraint will automatically be added to space.
        """
        assert isinstance(constraint, Constraint)
        if not (
            self.a is constraint.a
            and self.b is constraint.b
            or self.a is constraint.b
            and self.b is constraint.a
        ):
            raise ValueError("Constraint do not use the same bodies as joint")

        self._constraints.append(constraint)
        self._space.run_safe(self._add_constraint_to_space, constraint)
        return self

    def _add_constraint_to_space(self, constraint: Constraint) -> None:
        space = self.space
        space_ref = space._cffi_ref
        constraint_ref = constraint._cffi_ref
        lib.cpSpaceAddConstraint(space_ref, constraint_ref)
        constraint._space = space

    def remove_constraint(self: J, constraint: Constraint) -> J:
        """
        Detach constraint from space.
        """
        self._constraints.remove(constraint)
        constraint._joints = None
        self._space.run_safe(self._remove_constraint_from_space, constraint)
        return self

    def _remove_constraint_from_space(self, constraint):
        # During GC at program exit sometimes the constraint might already be removed.
        # Then skip this step.
        space = self.space
        space_ref = space._cffi_ref
        constraint_ref = constraint._cffi_ref
        constraint._space = None
        if lib.cpSpaceContainsConstraint(space_ref, constraint_ref):
            lib.cpSpaceRemoveConstraint(space_ref, constraint_ref)
