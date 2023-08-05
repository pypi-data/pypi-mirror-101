from dataclasses import dataclass
from typing import TYPE_CHECKING, Tuple, Any, overload, Union

from .shapes import Shape, shape_from_cffi
from ..cp import ffi, lib, cp_property, cpvec_property
from ..linalg import Vec2d, vec2d_from_cffi
from ..types import ContactPointSet, contact_point_set_from_cffi

if TYPE_CHECKING:
    from .space import Space
    from .body import Body


class ArbiterBase:
    """
    Common API for Arbiter and ArbiterProperties.
    """

    shapes: Tuple["Shape", "Shape"]
    normal: Vec2d

    @property
    def bodies(self) -> Tuple["Body", "Body"]:
        """
        Pair of bodies involved in collision.
        """
        s1, s2 = self.shapes
        return s1.body, s2.body

    @overload
    def other(self, obj: "Shape") -> "Shape":
        ...

    @overload
    def other(self, obj: "Body") -> "Body":
        ...

    def other(self, obj: Union["Body", "Shape"]):
        """
        Return other shape/body participating in collision.
        """
        if obj.is_body:
            a, b = self.bodies
        else:
            a, b = self.shapes

        if obj is a:
            return b
        elif obj is b:
            return a
        else:
            raise ValueError("object not present in arbiter")

    def normal_from(self, obj: Union["Shape", "Body"]) -> Vec2d:
        """
        Return normal vector leaving the specified shape or body.

        This is similar to the arb.normal property, but always choose the
        direction leaving the specified argument.
        """
        a, b = self.shapes
        if isinstance(obj, Shape):
            pass
        elif isinstance(obj, Body):
            a, b = a.body, b.body

        if obj is a:
            return self.normal
        elif obj is b:
            return -self.normal
        else:
            raise ValueError("object not present in arbiter")


class Arbiter(ArbiterBase):
    """The Arbiter object encapsulates a pair of colliding shapes and all of
    the data about their collision.

    They are created when a collision starts, and persist until those
    shapes are no longer colliding.

    Warning:
        Because arbiters are handled by the space you should never
        hold onto a reference to an arbiter as you don't know when it will be
        destroyed! Use them within the callback where they are given to you
        and then forget about them or copy out the information you need from
        them.

    .. note::
        You should never need to create an instance of this class directly.
    """

    __slots__ = "_cffi_maybe_ref", "_space"

    def _get_contact_point_set(self) -> ContactPointSet:
        points = lib.cpArbiterGetContactPointSet(self._cffi_ref)
        return contact_point_set_from_cffi(points)

    # noinspection PyPep8Naming
    def _set_contact_point_set(self, point_set: ContactPointSet) -> None:
        # This has to be done by fetching a new Chipmunk point set, update it
        # according to whats passed in and the pass that back to chipmunk due
        # to the fact that ContactPointSet doesnt contain a reference to the
        # corresponding c struct.
        cp_set = lib.cpArbiterGetContactPointSet(self._cffi_ref)
        cp_set.normal = point_set.normal

        if len(point_set.points) == cp_set.count:
            points = cp_set.points
            for i in range(cp_set.count):
                points[i].pointA = point_set.points[i].point_a
                points[i].pointB = point_set.points[i].point_b
                points[i].distance = point_set.points[i].distance
        else:
            msg = "Expected {} points, got {} points in point_set".format(
                cp_set.count, len(point_set.points)
            )
            raise Exception(msg)

        lib.cpArbiterSetContactPointSet(self._cffi_ref, ffi.addressof(cp_set))

    contact_point_set: ContactPointSet
    contact_point_set = property(  # type: ignore
        _get_contact_point_set,
        _set_contact_point_set,
        doc="""Contact point sets store information about contacts.
        
        Return `ContactPointSet`""",
    )
    restitution = cp_property[float](
        "cpArbiter(Get|Set)Restitution",
        doc="""The calculated restitution (elasticity) for this collision 
        pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        elasticity of the two shapes together.
        """,
    )
    friction = cp_property[float](
        "cpArbiter(Get|Set)Friction",
        doc="""The calculated friction for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        friction of the two shapes together.
        """,
    )
    surface_velocity = cpvec_property(
        "cpArbiter(Get|Set)SurfaceVelocity",
        doc="""The calculated surface velocity for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. the default calculation subtracts the 
        surface velocity of the second shape from the first and then projects 
        that onto the tangent of the collision. This is so that only 
        friction is affected by default calculation. Using a custom 
        calculation, you can make something that responds like a pinball 
        bumper, or where the surface velocity is dependent on the location 
        of the contact point.
        """,
        wrap=vec2d_from_cffi,
    )

    @property
    def total_impulse(self) -> Vec2d:
        """Returns the impulse that was applied this step to resolve the
        collision.

        This property should only be called from a post-solve or each_arbiter
        callback.
        """
        v = lib.cpArbiterTotalImpulse(self._cffi_ref)
        return Vec2d(v.x, v.y)

    @property
    def total_ke(self) -> float:
        """The amount of energy lost in a collision including static, but
        not dynamic friction.

        This property should only be called from a post-solve or each_arbiter callback.
        """
        return lib.cpArbiterTotalKE(self._cffi_ref)

    @property
    def is_first_contact(self) -> bool:
        """Returns true if this is the first step the two shapes started
        touching.

        This can be useful for sound effects for instance. If its the first
        frame for a certain collision, check the energy of the collision in a
        post_step() callback and use that to determine the volume of a sound
        effect to play.
        """
        return bool(lib.cpArbiterIsFirstContact(self._cffi_ref))

    @property
    def is_removal(self) -> bool:
        """Returns True during a separate() callback if the callback was
        invoked due to an object removal.
        """
        return bool(lib.cpArbiterIsRemoval(self._cffi_ref))

    @property
    def normal(self) -> Vec2d:
        """Returns the normal of the collision."""
        v = lib.cpArbiterGetNormal(self._cffi_ref)
        return Vec2d(v.x, v.y)

    @property
    def shapes(self) -> Tuple["Shape", "Shape"]:
        """
        Get the shapes in the order that they were defined in the
        collision handler associated with this arbiter
        """
        ptr_a = ffi.new("cpShape *[1]")
        ptr_b = ffi.new("cpShape *[1]")

        lib.cpArbiterGetShapes(self._cffi_ref, ptr_a, ptr_b)
        a = shape_from_cffi(ptr_a[0])
        b = shape_from_cffi(ptr_b[0])
        if a is None or b is None:
            raise ValueError("invalid shape in arbiter")
        return a, b

    @property
    def space(self) -> "Space":
        """
        The space the arbiter is attached to.
        """
        return self._space

    @property
    def _cffi_ref(self):
        ref = self._cffi_maybe_ref
        if ref is None:
            raise RuntimeError(
                "error trying to interact with dangling Arbiter.\n"
                "    You should never hold references live arbiters outside\n"
                "    collision handling functions. You may execute arb.copy()\n"
                "    if you need a copy of the arbiter state. The copy cannot\n"
                "    affect the collision."
            )
        return ref

    def __init__(self, ptr: Any, space: "Space"):
        self._cffi_maybe_ref = ptr
        self._space = space

    def close(self):
        """
        Disable arbiter so it cannot be used anymore.

        This function may be called to prevent unsafe handling of arbiter
        outside a callback function.

        Arbiter became unusable after calling this method.

        Use :meth:`copy` to retain a copy of all information in arbiter
        before destroying it. The copy only stores information and do not
        affect how collision is processed.
        """
        self._cffi_maybe_ref = None
        self._space = None

    def copy(self) -> "ArbiterProperties":
        """
        Return a copy of the arbiter that is safe to hold from outside a
        collision handler function and disable it.
        """
        new = ArbiterProperties.from_arbiter(self)
        self.close()
        return new


@dataclass(frozen=True)
class ArbiterProperties(ArbiterBase):
    """
    A data container will all properties of an arbiter.
    """

    @classmethod
    def from_arbiter(cls, arb: Arbiter):
        """
        Initialize properties from arbiter.
        """
        return cls(**{k: getattr(arb, k) for k in cls.__annotations__})

    contact_point_set: ContactPointSet
    restitution: float
    friction: float
    surface_velocity: Vec2d
    total_impulse: Vec2d
    total_ke: float
    is_first_contact: bool
    is_removal: bool
    normal: Vec2d
    shapes: Tuple["Shape", "Shape"]
    space: "Space"

    def copy(self):
        return self

    def close(self):
        """Do nothing."""
