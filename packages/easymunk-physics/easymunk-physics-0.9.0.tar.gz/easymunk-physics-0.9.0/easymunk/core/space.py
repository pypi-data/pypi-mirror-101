import logging
import platform
from collections import deque
from contextlib import contextmanager
from functools import cached_property
from itertools import chain
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    TypeVar,
    Iterable,
    Container,
    Iterator,
    Mapping,
    overload,
    Sequence,
)

import sidekick.api as sk

from ..cp import lib, ffi
from ..abc import CpCFFIBase, HasBBMixin, GameObjectInterface
from ..types import (
    BB,
    Shapes,
    Bodies,
    Constraints,
    contact_point_set_from_cffi,
    PointQueryInfo,
    SegmentQueryInfo,
    ShapeQueryInfo,
    ShapeFilter,
)
from .body import Body, CircleBody, SegmentBody, PolyBody, sort_body_pair
from .collision_handler import CollisionHandler
from .constraints import Constraint
from ..drawing import DrawOptions, get_drawing_options
from .junction import Junction
from .shapes import Shape, Circle, Segment, Poly, MakeShapeMixin, shape_from_cffi
from ..util import (
    void,
    init_attributes,
    cffi_body,
)
from ..linalg import Vec2d, vec2d_from_cffi
from ..typing import VecLike, BBLike

if TYPE_CHECKING:
    from .arbiter import Arbiter


# Types
ColType = Union[int, type(...)]
AddableObjects = Union[Body, Shape, Constraint]
BoolColHandlerCB = Callable[["Arbiter"], bool]
NullColHandlerCB = Callable[["Arbiter"], None]
ST = TypeVar("ST", bound="Space")
T = TypeVar("T")

# Constants
FILTER_ALL = ShapeFilter()
ALL_STEP_EVENTS = {"before-step", "before-sub-step", "after-sub-step", "after-step"}
SHAPE_TO_BODY = {Circle: CircleBody, Segment: SegmentBody, Poly: PolyBody}
NO_KWARGS = MappingProxyType({})

# Docs
POINT_QUERY_ARGS = """
        Args:
            point:
                Where to check for collision in the Space.
            distance:
                Match within this tolerance. If a distance of 0.0 is used, the
                point must lie inside a shape. Negative values mean that
                the point must be a under a certain depth within a shape to be
                considered a match.
            filter:
                Only pick shapes matching the filter.
"""

COLLISION_HANDLER_KWARGS = """
    Keyword Args:
            begin:
                Handler callback called before the first frame of collision
            pre_solve:
                Handler callback called before each frame
            post_solve:
                Handler callback called after each frame
            separate:
                Handler callback called after the final frame
"""

COLLISION_DECORATOR_ARGS = """
        Similar decorators exist for begin/pre_solve/post_solve/separate events.

        Args:
            a:
                Collision type. Can be set to Ellipsis (...) to accept all
                shapes.
            b:
                Collision type. Can be set to Ellipsis (...) to accept all
                shapes. If both a and b are Ellipsis, it register the default
                collision handler like in :meth:`default_collision_handler`. 
                This method controls the dispatch mechanism for collision 
                handlers and should be used with care.
        
        Positional and keyword arguments are forwarded to function.
"""


class Space(
    MakeShapeMixin[CircleBody, SegmentBody, PolyBody],
    GameObjectInterface,
    HasBBMixin,
    CpCFFIBase,
):
    """Spaces are the basic unit of simulation. You add rigid bodies, shapes
    and joints to it and then step them all forward together through time.

    A Space can be copied and pickled. Note that some internal collision cache
    data is not copied, which can make the simulation a bit unstable the
    first few steps of the fresh copy.

    Custom properties set on the space will also be copied/pickled and any
    collision handlers will also be copied/pickled. Note that depending on
    the pickle protocol used there are some restrictions on what functions can
    be copied/pickled.
    """

    is_space = True
    _pickle_format_version = 0
    _pickle_args = ("threaded",)
    _pickle_kwargs = (
        "iterations",
        "gravity",
        "damping",
        "idle_speed_threshold",
        "sleep_time_threshold",
        "collision_slop",
        "collision_bias",
        "collision_persistence",
        "threads",
    )
    _pickle_meta_hide = {
        "_bodies",
        "_cffi_ref",
        "_forces",
        "_handlers",
        "_locked",
        "bodies",
        "constraints",
        "shapes",
        "static_body",
    }
    _init_kwargs = {
        *_pickle_args,
        *_pickle_kwargs,
        "elasticity",
        "friction",
        "draw_options",
    }
    iterations: int
    iterations = property(  # type: ignore
        lambda self: lib.cpSpaceGetIterations(self._cffi_ref),
        lambda self, value: void(lib.cpSpaceSetIterations(self._cffi_ref, value)),
        doc="""Iterations allow you to control the accuracy of the solver.

        Defaults to 10.

        Pymunk uses an iterative solver to figure out the forces between
        objects in the space. What this means is that it builds a big list of
        all of the collisions, joints, and other constraints between the
        bodies and makes several passes over the list considering each one
        individually. The number of passes it makes is the iteration count,
        and each iteration makes the solution more accurate. If you use too
        many iterations, the physics should look nice and solid, but may use
        up too much CPU time. If you use too few iterations, the simulation
        may seem mushy or bouncy when the objects should be solid. Setting
        the number of iterations lets you balance between CPU usage and the
        accuracy of the physics. Pymunk's default of 10 iterations is
        sufficient for most simple games.
        """,
    )
    gravity: Vec2d
    gravity = property(  # type: ignore
        lambda self: vec2d_from_cffi(lib.cpSpaceGetGravity(self._cffi_ref)),
        lambda self, g: void(lib.cpSpaceSetGravity(self._cffi_ref, g)),
        doc="""Global gravity applied to the space.

        Defaults to (0,0). Can be overridden on a per body basis by writing
        custom integration functions and set it on the body:
        :py:meth:`easymunk.Body.velocity_func`.
        """,
    )
    damping: float
    damping = property(  # type: ignore
        lambda self: lib.cpSpaceGetDamping(self._cffi_ref),
        lambda self, damping: void(lib.cpSpaceSetDamping(self._cffi_ref, damping)),
        doc="""Damping to apply to the space.

        A value of 0.9 means that each body will lose 10% of its velocity per
        second. Defaults to 1. Like gravity, it can be overridden on a per
        body basis.
        """,
    )
    idle_speed_threshold: float
    idle_speed_threshold = property(  # type: ignore
        lambda self: lib.cpSpaceGetIdleSpeedThreshold(self._cffi_ref),
        lambda self, value: void(
            lib.cpSpaceSetIdleSpeedThreshold(self._cffi_ref, value)
        ),
        doc="""Speed threshold for a body to be considered idle.

        The default value of 0 means the space estimates a good threshold
        based on gravity.
        """,
    )
    sleep_time_threshold: float
    sleep_time_threshold = property(  # type: ignore
        lambda self: lib.cpSpaceGetSleepTimeThreshold(self._cffi_ref),
        lambda self, value: void(
            lib.cpSpaceSetSleepTimeThreshold(self._cffi_ref, value)
        ),
        doc="""Time a group of bodies must remain idle in order to fall
        asleep.

        The default value of `inf` disables the sleeping algorithm.
        """,
    )
    collision_slop: float
    collision_slop = property(  # type: ignore
        lambda self: lib.cpSpaceGetCollisionSlop(self._cffi_ref),
        lambda self, value: void(lib.cpSpaceSetCollisionSlop(self._cffi_ref, value)),
        doc="""Amount of overlap between shapes that is allowed.

        To improve stability, set this as high as you can without noticeable
        overlapping. It defaults to 0.1.
        """,
    )
    collision_bias: float
    collision_bias = property(  # type: ignore
        lambda self: lib.cpSpaceGetCollisionBias(self._cffi_ref),
        lambda self, value: void(lib.cpSpaceSetCollisionBias(self._cffi_ref, value)),
        doc="""Determines how fast overlapping shapes are pushed apart.

        Pymunk allows fast moving objects to overlap, then fixes the overlap
        over time. Overlapping objects are unavoidable even if swept
        collisions are supported, and this is an efficient and stable way to
        deal with overlapping objects. The bias value controls what
        percentage of overlap remains unfixed after a second and defaults
        to ~0.2%. Valid values are in the range from 0 to 1, but using 0 is
        not recommended for stability reasons. The default value is
        calculated as cpfpow(1.0f - 0.1f, 60.0f) meaning that pymunk attempts
        to correct 10% of error ever 1/60th of a second.

        ..Note::
            Very very few games will need to change this value.
        """,
    )
    collision_persistence: int
    collision_persistence = property(  # type: ignore
        lambda self: lib.cpSpaceGetCollisionPersistence(self._cffi_ref),
        lambda self, value: void(
            lib.cpSpaceSetCollisionPersistence(self._cffi_ref, value)
        ),
        doc="""The number of frames the space keeps collision solutions
        around for.

        Helps prevent jittering contacts from getting worse. This defaults
        to 3.

        ..Note::
            Very very few games will need to change this value.
        """,
    )
    current_time_step: int
    current_time_step = property(  # type: ignore
        lambda self: lib.cpSpaceGetCurrentTimeStep(self._cffi_ref),
        doc="""Retrieves the current (if you are in a callback from
        Space.step()) or most recent (outside of a Space.step() call)
        timestep.
        """,
    )
    threads: int
    threads = property(  # type: ignore
        lambda self: int(lib.cpHastySpaceGetThreads(self._cffi_ref))
        if self.threaded
        else 1,
        lambda self, n: void(
            self.threaded and lib.cpHastySpaceSetThreads(self._cffi_ref, n)
        ),
        doc="""The number of threads to use for running the step function. 
        
        Only valid when the Space was created with threaded=True. Currently the 
        max limit is 2, setting a higher value wont have any effect. The 
        default is 1 regardless if the Space was created with threaded=True, 
        to keep determinism in the simulation. Note that Windows does not 
        support the threaded solver.
        """,
    )

    @property
    def shapes(self) -> Shapes:
        """A list of all the shapes added to this space

        (includes both static and non-static)
        """
        return Shapes(self, self._iter_shapes)

    @property
    def bodies(self) -> Bodies:
        """A list of the bodies added to this space"""
        return Bodies(self, self._bodies.__iter__)

    @property
    def constraints(self) -> Constraints:
        """A list of the constraints added to this space"""
        return Constraints(self, self._iter_constraints)

    @cached_property
    def static_body(self) -> Body:
        """A dedicated static body for the space.

        You don't have to use it, but many times it can be convenient to have
        a static body together with the space.
        """
        body = Body(body_type=Body.STATIC)
        body._space = self

        lib.cpSpaceAddBody(self._cffi_ref, cffi_body(body))
        return body

    @property
    def kinetic_energy(self):
        """
        Total kinetic energy of dynamic bodies.
        """
        bodies = self.bodies.filter(body_type=Body.DYNAMIC)
        return sum(b.kinetic_energy for b in bodies)

    @property
    def gravitational_energy(self):
        """
        Potential energy of dynamic bodies due to gravity.
        """
        bodies = self.bodies.filter(body_type=Body.DYNAMIC)
        return sum(b.gravitational_energy for b in bodies)

    @property
    def potential_energy(self):
        """
        Sum of gravitational energy and all tracked sources of potential
        energies.
        """
        energy = self.gravitational_energy
        # TODO: implement external forces
        # for force in self._forces:
        #     try:
        #         acc = force.potential_energy
        #     except AttributeError:
        #         pass
        #     else:
        #         energy += acc
        return energy

    @property
    def energy(self):
        """
        The sum of kinetic and potential energy.
        """
        return self.potential_energy + self.kinetic_energy

    @property
    def center_of_gravity(self):
        """
        Center of mass position of all dynamic objects.
        """
        m_acc = 0.0
        pos_m_acc = Vec2d(0, 0)
        for o in self.bodies.filter(body_type=Body.DYNAMIC):
            m_acc += o.mass
            pos_m_acc += o.mass * o.local_to_world(o.center_of_gravity)
        return pos_m_acc / m_acc

    @property
    def linear_momentum(self):
        """
        Total Linear momentum assigned to dynamic objects.
        """
        momentum = Vec2d(0, 0)
        for o in self.bodies.filter(body_type=Body.DYNAMIC):
            momentum += o.mass * o.velocity
        return momentum

    @property
    def angular_momentum(self):
        """
        Total angular momentum assigned to dynamic objects.
        """
        momentum = 0.0
        for o in self.bodies.filter(body_type=Body.DYNAMIC):
            momentum += o.moment * o.angular_velocity
            momentum += o.local_to_world(o.center_of_gravity).cross(o.velocity)
        return momentum

    #
    # Default values for rarely used variables.
    #
    draw_options: Optional["DrawOptions"] = None
    name: str = None
    color: Any = None
    description: str = ""
    _named_bodies: Dict[str, Body]
    _named_bodies = sk.lazy(lambda self: {})  # type: ignore

    def __init__(self, threaded: bool = False, **kwargs) -> None:
        """Create a new instance of the Space.

        If you set threaded=True the step function will run in threaded mode
        which might give a speedup. Note that even when you set threaded=True
        you still have to set Space.threads=2 to actually use more than one
        thread.

        Also note that threaded mode is not available on Windows, and setting
        threaded=True has no effect on that platform.
        """

        self.threaded = threaded and platform.system() != "Windows"
        if self.threaded:
            cp_space = lib.cpHastySpaceNew()
            freefunc = lib.cpHastySpaceFree
        else:
            cp_space = lib.cpSpaceNew()
            freefunc = lib.cpSpaceFree
        self._cffi_ref: Any = ffi.gc(cp_space, cffi_free_space(freefunc))

        # To prevent the gc to collect the callbacks.
        self._collision_handlers: Dict[Any, CollisionHandler] = {}
        self._event_handlers: Dict[str, List[Callable[..., None]]] = {}
        self._bodies: Set[Body] = set()
        self._junctions: Dict[Tuple[Body, Body], Junction] = {}
        self._run_later: List[Callable[[], None]] = []
        self._locked: bool = False
        self.time: float = 0.0

        # Save attributes
        init_attributes(self, self._init_kwargs, kwargs)

    def __repr__(self):
        args = []
        if name := self.name:
            args.append(f"name={name!r}")
        if descr := self.description:
            args.append(f"description={descr!r}")
        cls = type(self).__name__
        args = ", ".join(args) if args else "..."
        return f"{cls}({args})"

    def __getstate__(self):
        args, meta = super().__getstate__()
        meta["$objects"] = {
            "body": [*self._bodies, self.__dict__.get("static_body")],
            "constraint": [*self._iter_constraints()],
            "collision": {k: v.as_dict() for k, v in self._collision_handlers.items()},
            "event": {k: lst[:] for k, lst in self._event_handlers.items()},
        }
        return self._pickle_format_version, args, meta

    def __setstate__(self, state) -> None:
        version, args, meta = state
        if version != self._pickle_format_version:
            expect = self._pickle_format_version
            raise ValueError(f"invalid pickle version: {version}, expect {expect}.")

        # Keep for later
        objects = meta.pop("$objects")
        super().__setstate__((args, meta))

        # Add bodies to space
        static = objects["body"].pop()
        if static is not None:
            self.add_body(static)
            self.__dict__["static_body"] = static
            self._bodies.discard(static)
        for body in objects["body"]:
            self.add_body(body)

        # Add constraints
        for cons in objects["constraint"]:
            self.junction(cons.a, cons.b).add_constraint(cons)

        # Register collision handlers
        for k, data in objects["collision"].items():
            if k is None:
                handler = self.default_collision_handler()
            elif isinstance(k, tuple):
                handler = self.collision_handler(*k)
            else:
                handler = self.wildcard_collision_handler(k)
            handler.update(data)

        # Update event handlers
        self._event_handlers.update(objects["event"])

    def __getitem__(self, name):
        return self._named_bodies[name]

    def _create_shape(self, cls, args, kwargs):
        space = kwargs.pop("space", self)

        try:
            body = kwargs.pop("body")
        except KeyError:
            factory = kwargs.pop("cls", SHAPE_TO_BODY[cls])
            body = factory(*args, **kwargs)
        else:
            # noinspection PyProtectedMember
            opts = Body._extract_options(kwargs)
            if opts:
                raise TypeError(f"cannot set parameter to body: {set(opts)}")
            if body == "static_body":
                body = self.static_body
            if body.body_type == Body.DYNAMIC and body.mass == 0:
                kwargs.setdefault("density", 1.0)
            cls(*args, body=body, **kwargs)

        if space is self:
            self.add(body)
        elif space is not None:
            raise ValueError(f"cannot add to a different space: {space!r}")
        return body

    def _iter_bounding_boxes(self, cached) -> Iterable["BB"]:
        if cached:
            for shape in self._iter_shapes():
                if not shape.sensor:
                    yield shape.cache_bb()
        else:
            for shape in self._iter_shapes():
                if not shape.sensor:
                    yield shape.bb

    def _iter_constraints(self) -> Iterable["Constraint"]:
        return chain.from_iterable(self._junctions.values())

    def _iter_shapes(self) -> Iterator["Shape"]:
        for body in self._bodies:
            yield from body._iter_shapes()

    def _iter_arbiters(self) -> Iterator["Arbiter"]:
        for body in self._bodies:
            yield from body.arbiters

    def _iter_game_object_children(self):
        yield from self._bodies
        yield from self._junctions.values()

    def _describe_body(self, indent, memo) -> List[str]:
        if self.description:
            yield ""
        yield indent + "# PROPERTIES"
        yield from super()._describe_body(indent, memo)

        yield ""
        yield indent + "# BODIES"
        for i, b in enumerate(self.bodies, 1):
            for ln in b.describe(name=f"[{i}]").splitlines():
                yield indent + ln

    @contextmanager
    def locked(self):
        """
        A context manager that locks space inside a with block.

        >>> space = mk.Space()
        >>> with space.locked():
        ...     do_something()

        This is mostly an internal API and is used to defend against unsafe
        calls to functions that may run during simulation step.
        """
        locked = self._locked
        self._locked = True
        yield self
        self._locked = locked

    def create_body(
        self, mass: float = 0, moment: float = 0, body_type=Body.DYNAMIC, **kwargs
    ) -> Body:
        """
        Create a new body in space with no shapes attached to it.
        """
        space = kwargs.pop("space", self)
        body = Body(mass, moment, body_type, **kwargs)
        if space is self:
            self.add(body)
        elif space is not None:
            raise TypeError("cannot add body to a different space.")
        return body

    def create_path(
        self,
        vertices: List[VecLike],
        close: bool = False,
        static_body: bool = False,
        **kwargs,
    ) -> Tuple["Body", List["Shape"]]:
        """
        Create path by connecting several Segment shapes to a body.

        Return the resulting path and a containing body.

        Args:
            vertices: List of vertices that forms path.
            close: If True (not default), create a closed loop.
            static_body: If True (not default), attach paths to the space's
                static_body instead of creating a new body.

        Keyword Args:
            Accepts all arguments for :cls:`SegmentBody`.
        """
        if not vertices:
            raise ValueError("empty path")

        if close:
            vertices = list(vertices)
            vertices.append(vertices[0])

        if static_body:
            body = self.static_body
        else:
            opts = Body._extract_options(kwargs)
            opts.setdefault("body_type", "static")
            body = self.create_body(opts)

        a, bs = sk.uncons(vertices)
        segments = []
        for b in bs:
            segments.append(body.create_segment(a, b, **kwargs))
            a = b
        return body, segments

    def create_margin(self, bb: BBLike, **kwargs) -> Tuple["Body", List["Shape"]]:
        """
        Create paths from bounding box. Accept the same arguments of :meth:`create_path`.
        """
        x, y, x_, y_ = bb
        path = [(x, y), (x_, y), (x_, y_), (x, y_)]
        return self.create_path(path, close=True, **kwargs)

    def junction(self, a: Body, b: Body) -> Junction:
        """
        Return the joint between body a and body b.

        Joint objects are used to hold constraints between pairs of objects.
        """
        key = sort_body_pair(a, b)
        try:
            junction = self._junctions[key]
        except KeyError:
            if a is b:
                raise ValueError("cannot create a joint with itself")
            self._junctions[key] = junction = Junction(a, b, self)
            a._connected_bodies.add(b)
            b._connected_bodies.add(a)

        return junction if junction.a is a else junction.flipped

    def detach(self: T) -> T:
        # A NO-OP for space instances
        return self

    def add(self: ST, *objs: AddableObjects, add_children=True) -> ST:
        """Add one or many shapes, bodies or constraints (joints) to the space

        Unlike Chipmunk and earlier versions of pymunk its now allowed to add
        objects even from a callback during the simulation step. However, the
        add will not be performed until the end of the step.
        """

        objs = deque(objs)
        while objs:
            obj = objs.popleft()

            if obj.space is self:
                continue
            elif obj.space is not None:
                raise ValueError(f"object already in another space: {obj.space!r}")

            if isinstance(obj, Body):
                self.add_body(obj)
            elif isinstance(obj, Shape):
                if obj.body is None:
                    raise ValueError("cannot add shape without body")
                if obj.body.space is self:
                    obj.body.add_shape(obj)
                else:
                    space = obj.body.space
                    raise ValueError(f"shape in body of a different space: {space}")
            elif isinstance(obj, Constraint):
                self.junction(obj.a, obj.b).add_constraint(obj)
            else:
                cls = type(obj).__name__
                raise ValueError(f"cannot add to space: {cls}")

        return self

    def remove(self: ST, *objs: AddableObjects, remove_children=True) -> ST:
        """Remove one or many shapes, bodies or constraints from the space

        If called from callback during update step, the removal will not be
        performed until the end of the step.

        .. Note::
            When removing objects from the space, make sure you remove any
            other objects that reference it. For instance, when you remove a
            body, remove the joints and shapes attached to it.
        """
        for obj in objs:
            if obj.space is not None:
                obj.detach()
        return self

    def discard(self: ST, *objs: AddableObjects, remove_children=True) -> ST:
        """
        Discard objects from space.

        Similar to remove, but do not throw errors if element is not present
        in space.
        """
        return self._remove_or_discard(objs, remove_children, True)

    def add_body(self, body: "Body") -> None:
        if body.space is self:
            return

        name = body.name
        if name is not None:
            if name in self._named_bodies:
                raise ValueError(f"space already has a body named {name!r}")
            self._named_bodies[name] = body

        self._bodies.add(body)
        self.run_safe(self._add_body_to_space, body)

    def _add_body_to_space(self, body):
        body._space = self
        lib.cpSpaceAddBody(self._cffi_ref, body._cffi_ref)
        for shape in body.shapes:
            body.add_shape(shape)

    def reindex_shape(self: ST, shape: Shape) -> ST:
        """Update the collision detection data for a specific shape in the
        space.
        """
        lib.cpSpaceReindexShape(self._cffi_ref, shape._cffi_ref)
        return self

    def reindex_shapes_for_body(self: ST, body: Body) -> ST:
        """Reindex all the shapes for a certain body."""
        lib.cpSpaceReindexShapesForBody(self._cffi_ref, body._cffi_ref)
        return self

    def reindex_static(self: ST) -> ST:
        """Update the collision detection info for the static shapes in the
        space. You only need to call this if you move one of the static shapes.
        """
        lib.cpSpaceReindexStatic(self._cffi_ref)
        return self

    def use_spatial_hash(self: ST, dim: float, count: int) -> ST:
        """Switch the space to use a spatial hash instead of the bounding box
        tree.

        Easymunk supports two spatial indexes. The default is an axis-aligned
        bounding box tree inspired by the one used in the Bullet Physics
        library, but caching of overlapping leaves was added to give it very
        good temporal coherence. The tree requires no tuning, and most games
        will find that they get the best performance using from the tree. The
        other available spatial index type available is a spatial hash, which
        can be much faster when you have a very large number (1000s) of
        objects that are all the same size. For smaller numbers of objects,
        or objects that vary a lot in size, the spatial hash is usually much
        slower. It also requires tuning (usually through experimentation) to
        get the best possible performance.

        The spatial hash data is fairly size sensitive. dim is the size of
        the hash cells. Setting dim to the average collision shape size is
        likely to give the best performance. Setting dim too small will cause
        the shape to be inserted into many cells, setting it too low will
        cause too many objects into the same hash slot.

        count is the suggested minimum number of cells in the hash table. If
        there are too few cells, the spatial hash will return many false
        positives. Too many cells will be hard on the cache and waste memory.
        Setting count to ~10x the number of objects in the space is probably a
        good starting point. Tune from there if necessary.

        Args:
            dim: the size of the hash cells
            count: the suggested minimum number of cells in the hash table
        """
        lib.cpSpaceUseSpatialHash(self._cffi_ref, dim, count)
        return self

    #
    # Control iterations and evolution
    #
    def step(
        self: ST,
        dt: float,
        sub_steps: int = 1,
        skip_events: Union[bool, Container[str]] = False,
    ) -> ST:
        """Update the space for the given time step.

        Using a fixed time step is highly recommended. Doing so will increase
        the efficiency of the contact persistence, requiring an order of
        magnitude fewer iterations to resolve the collisions in the usual case.

        It is not the same to call step 10 times with a dt of 0.1 and
        calling it 100 times with a dt of 0.01 even if the end result is
        that the simulation moved forward 100 units. Performing  multiple
        calls with a smaller dt creates a more stable and accurate
        simulation. Therefore it sometimes make sense to have a little for loop
        around the step call, like in this example:

        >>> s = mk.Space()
        >>> steps = 4
        >>> for _ in range(steps):
        ...     s.step(0.25)
        Space(...)
        >>> s.time
        1.0

        Args:
            dt:
                Time step length
            sub_steps:
                Number n of sub-steps of size dt/n to perform. The number of
                sub-steps determine a tradeoff between accuracy (large n) and
                speed (small n).

                For games, it is common to synchronize the step size to the
                mainloop and choose the smaller number of sub-steps that makes
                the physics stable.

                The solver behaves poorly if either the step size or the number
                of sub-steps is changed during simulation. Varying it in a way
                that keeps the size of each sub-step fixed is acceptable.
            skip_events:
                If true, skip calling the before/after-step/sub-step callbacks.
                It can be a sequence of strings for events to skip. E.g.:
                skip_events=["before-step", "after-step"] will skip callbacks
                scheduled to execute before and after a full step, but keep
                executing callbacks for sub-steps.
        """
        if sub_steps <= 0:
            raise ValueError("sub-steps must be greater than or equal to 1")
        dt /= sub_steps

        if skip_events is False:
            skip_events = ()
        elif skip_events is False:
            skip_events = ALL_STEP_EVENTS

        self._execute_step_handlers("before-step", skip_events)
        for _ in range(sub_steps):
            self._execute_step_handlers("before-sub-step", skip_events)
            try:
                self._locked = True
                if self.threaded:
                    lib.cpHastySpaceStep(self._cffi_ref, dt)
                else:
                    lib.cpSpaceStep(self._cffi_ref, dt)
                self.time += dt
                self._removed_shapes = {}
            finally:
                self._locked = False

            for fn in self._run_later:
                fn()
            self._run_later.clear()
            self._execute_step_handlers("after-sub-step", skip_events)
        self._execute_step_handlers("after-step", skip_events)
        return self

    def _execute_step_handlers(self, key: str, skip_events: Container[str] = ()):
        if key in skip_events:
            return
        try:
            lst = self._event_handlers[key]
        except KeyError:
            return

        bad_positions = []
        try:
            for i, fn in enumerate(lst):
                try:
                    fn()
                except StopIteration:
                    bad_positions.append(i)
        finally:
            while bad_positions:
                del lst[bad_positions.pop()]

    def loop(
        self,
        dt: float,
        n_steps: int = None,
        sub_steps: int = 1,
        stop: Callable[["Space"], bool] = lambda _: False,
    ) -> None:
        """
        Run simulation for n_steps of duration dt.

        Args:
            dt: Duration of each step.
            n_steps: maximum number of steps. Loops forever, if not given.
            sub_steps: Number of sub-steps at each iteration.
            stop: A function (Space) -> bool that controls when to stop iteration.
        """
        if n_steps is None:
            while not stop(self):
                self.step(dt, sub_steps)
        else:
            for _ in range(n_steps):
                if stop(self):
                    break
                self.step(dt, sub_steps)

    def before_step(self, opt=None, /, args=None, kwargs=None, sub_steps=False):
        """
        Decorates function that is executed before each step.

        Args:
            opt:
                Control how function is interpreted.
                * 'generator': Expect a generator function and executes a
                  single iteration per step.
            args:
                A tuple of positional arguments passed to function.
            kwargs:
                A mapping of keyword arguments passsed to function.
            sub_steps:
                If True, function is also executed in sub-steps.

        >>> space = mk.Space()
        >>> @space.before_step()
        ... def debug():
        ...     print('Executing new frame!')
        """
        ev = "before-sub-step" if sub_steps else "before-step"
        return self._step_decorator(ev, opt, args, kwargs)

    def after_step(self, opt=None, /, args=None, kwargs=None, sub_steps=False):
        """
        Decorates function that is executed after each step.

        Accepts the same arguments as :meth:`before_step`

        >>> space = mk.Space()
        >>> @space.after_step()
        ... def debug():
        ...     print('Executing new frame!')
        """
        ev = "after-sub-step" if sub_steps else "after-step"
        return self._step_decorator(ev, opt, args, kwargs)

    def run_safe(self: ST, fn, /, *args, **kwargs) -> ST:
        """
        Run function immediately if space is not locked (i.e. during a step),
        or schedule it to run just after step finishes.
        """
        if self._locked:
            if args or kwargs:
                fn = sk.partial(fn, *args, **kwargs)
            self._run_later.append(fn)
        else:
            fn(*args, **kwargs)
        return self

    def _step_decorator(self, event, opt, args, kwargs):
        def decorator(fn):
            if args or kwargs:
                cb = sk.partial(fn, *(args or ()), **(kwargs or {}))
            else:
                cb = fn
            self._register_step_handler(event, opt, cb)
            return fn

        return decorator

    def _register_step_handler(self, event, opt, fn):
        lst = self._event_handlers.setdefault(event, [])
        if opt == "generator":
            cb = fn().__next__
        elif opt is None:
            cb = fn
        else:
            raise ValueError(f"invalid option: {opt!r}")

        lst.append(cb)

    #
    # Collision handlers
    #
    def collision_handler(self, a: ColType, b: ColType, **kwargs) -> CollisionHandler:
        f"""
        Get/define the :py:class:`CollisionHandler` for collisions between
        objects of type "a" and "b".

        Fill the desired collision callback functions, for details see the
        :py:class:`CollisionHandler` object.

        Whenever shapes with collision types (:py:attr:`Shape.collision_type`)
        a and b collide, this handler will be used to process the collision
        events. When a new collision handler is created, the callbacks will all be
        set to builtin callbacks that perform the default behavior (call the
        wildcard handlers, and accept all collisions).

        Args:
            a: Collision type a
            b: Collision type b

        {COLLISION_HANDLER_KWARGS}
        """

        key = min(a, b), max(a, b)
        try:
            handler = self._collision_handlers[key]
        except KeyError:
            ptr = lib.cpSpaceAddCollisionHandler(self._cffi_ref, a, b)
            self._collision_handlers[key] = handler = CollisionHandler(ptr, self)

        handler.update(kwargs)
        return handler

    def wildcard_collision_handler(self, col_type: int, **kwargs) -> CollisionHandler:
        f"""
        Get/define the wildcard collision handler for given collision type.

        This handler will be used any time an object with this type collides
        with another object, regardless of its type. A good example is a
        projectile that should be destroyed the first time it hits anything.
        There may be a specific collision handler and two wildcard handlers.
        It's up to the specific handler to decide if and when to call the
        wildcard handlers and what to do with their return values.

        When a new wildcard handler is created, the callbacks will all be
        set to builtin callbacks that perform the default behavior. (accept
        all collisions in :py:func:`~CollisionHandler.begin` and
        :py:func:`~CollisionHandler.pre_solve`, or do nothing for
        :py:func:`~CollisionHandler.post_solve` and
        :py:func:`~CollisionHandler.separate`.

        Args:
            col_type: Collision type

        {COLLISION_HANDLER_KWARGS}
        """

        try:
            handler = self._collision_handlers[col_type]
        except KeyError:
            ptr = lib.cpSpaceAddWildcardHandler(self._cffi_ref, col_type)
            self._collision_handlers[col_type] = handler = CollisionHandler(ptr, self)

        handler.update(kwargs)
        return handler

    def default_collision_handler(self, **kwargs) -> CollisionHandler:
        f"""
        Return a reference to the default collision handler or that is
        used to process all collisions that don't have a more specific
        handler.

        The default behavior for each of the callbacks is to call
        the wildcard handlers, ANDing their return values together if
        applicable.

        {COLLISION_HANDLER_KWARGS}
        """

        try:
            handler = self._collision_handlers[None]
        except KeyError:
            ptr = lib.cpSpaceAddDefaultCollisionHandler(self._cffi_ref)
            self._collision_handlers[None] = handler = CollisionHandler(ptr, self)
        handler.update(kwargs)
        return handler

    @overload
    def begin_collision(
        self,
        a: ColType,
        b: ColType,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> Callable[[BoolColHandlerCB], BoolColHandlerCB]:
        ...

    @overload
    def begin_collision(
        self,
        a: ColType,
        b: ColType,
        func: BoolColHandlerCB,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> BoolColHandlerCB:
        ...

    def begin_collision(self, a, b, func=None, /, args=(), kwargs=NO_KWARGS):
        f"""
        Decorates function that is executed when collision starts.

        Collision handler must return a boolean to decide if collision should be
        resolved or not.
        {COLLISION_DECORATOR_ARGS}

        >>> space = mk.Space()
        >>> @space.begin_collision(1, 2)
        ... def debug(arb):
        ...     print('collision between col_type=1 and col_type=2')
        ..      return True

        The Ellipsis symbol (...) can be used to register wildcard collisions like so

        >>> space = mk.Space()
        >>> @space.begin_collision(1, ...)
        ... def debug(arb):
        ...     print('col_type=1 caught on collision')
        ..      return True
        """
        if func:
            return self._collision_handler("begin", func, (a, b), args, kwargs)
        return lambda fn: self.begin_collision(a, b, fn, args, kwargs)

    @overload
    def pre_solve_collision(
        self,
        a: ColType,
        b: ColType,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> Callable[[BoolColHandlerCB], BoolColHandlerCB]:
        ...

    @overload
    def pre_solve_collision(
        self,
        a: ColType,
        b: ColType,
        func: BoolColHandlerCB,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> BoolColHandlerCB:
        ...

    def pre_solve_collision(self, a, b, func=None, /, args=(), kwargs=NO_KWARGS):
        f"""
        Decorates function that is executed when collision starts.

        Collision handler must return a boolean to decide if collision should be
        resolved or not.
        {COLLISION_DECORATOR_ARGS}

        >>> space = mk.Space()
        >>> @space.pre_solve_collision(1, 2)
        ... def debug(arb):
        ...     print('collision between col_type=1 and col_type=2')
        ...     return True
        """
        if func:
            return self._collision_handler("pre_solve", func, (a, b), args, kwargs)
        return lambda fn: self.pre_solve_collision(a, b, fn, args, kwargs)

    @overload
    def post_solve_collision(
        self,
        a: ColType,
        b: ColType,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> Callable[[NullColHandlerCB], NullColHandlerCB]:
        ...

    @overload
    def post_solve_collision(
        self,
        a: ColType,
        b: ColType,
        func: NullColHandlerCB,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> NullColHandlerCB:
        ...

    def post_solve_collision(self, a, b, func=None, /, args=(), kwargs=NO_KWARGS):
        f"""
        Decorates function that is executed each frame after solving impulses.

        {COLLISION_DECORATOR_ARGS}

        >>> space = mk.Space()
        >>> @space.post_solve_collision(1, 2)
        ... def debug(arb):
        ...     print('collision between col_type=1 and col_type=2')
        """
        if func:
            return self._collision_handler("post_solve", func, (a, b), args, kwargs)
        return lambda fn: self.post_solve_collision(a, b, fn, args, kwargs)

    @overload
    def separate_collision(
        self,
        a: ColType,
        b: ColType,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> Callable[[NullColHandlerCB], NullColHandlerCB]:
        ...

    @overload
    def separate_collision(
        self,
        a: ColType,
        b: ColType,
        func: NullColHandlerCB,
        /,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] = NO_KWARGS,
    ) -> NullColHandlerCB:
        ...

    def separate_collision(self, a, b, func=None, /, args=(), kwargs=NO_KWARGS):
        f"""
        Decorates function that is executed after shapes loose contact.

        {COLLISION_DECORATOR_ARGS}

        >>> space = mk.Space()
        >>> @space.separate_collision(1, 2)
        ... def debug(arb):
        ...     print('collision between col_type=1 and col_type=2')
        """
        if func:
            return self._collision_handler("separate", func, (a, b), args, kwargs)
        return lambda fn: self.separate_collision(a, b, fn, args, kwargs)

    def _collision_handler(self, event, fn, which, args, kwargs):
        if args or kwargs:
            fn = sk.partial(fn, *args, **kwargs)
        opts = {event: fn}

        which = [x for x in which if x is not ...]
        if len(which) == 0:
            handler = self.default_collision_handler(**opts)
        elif len(which) == 1:
            handler = self.wildcard_collision_handler(*which, **opts)
        elif len(which) == 2:
            handler = self.collision_handler(*which, **opts)
        else:
            n = len(which)
            raise ValueError(f"accepts at most 2 collision types, got {n}")

        fn.handler = handler
        return fn

    # noinspection PyShadowingBuiltins
    def point_query(
        self, point: VecLike, distance: float = 0, filter: ShapeFilter = FILTER_ALL
    ) -> List[PointQueryInfo]:
        f"""Query space at point for shapes within the given distance range.

        The filter is applied to the query and follows the same rules as the
        collision detection. See :py:class:`ShapeFilter` for details about how
        the shape_filter parameter can be used.

        {POINT_QUERY_ARGS}

        Note:
            Sensor shapes are included in the result (In
            :py:meth:`Space.point_query_nearest` they are not)

        Result:
            A list of point queries.
        """

        @ffi.callback("cpSpacePointQueryFunc")
        def cb(ptr, vec, dist, gradient, _data):
            shape = shape_from_cffi(ptr)
            if shape:
                vec = Vec2d(vec.x, vec.y)
                gradient = Vec2d(gradient.x, gradient.y)
                result.append(PointQueryInfo(shape, vec, dist, gradient))

        result: List[PointQueryInfo] = []
        data = ffi.new_handle(self)
        lib.cpSpacePointQuery(self._cffi_ref, point, distance, filter, cb, data)
        return result

    # noinspection PyShadowingBuiltins
    def point_query_nearest(
        self, point: VecLike, distance: float = 0.0, filter: ShapeFilter = FILTER_ALL
    ) -> Optional[PointQueryInfo]:
        f"""Query space at point the nearest shape within the given distance
        range.

        {POINT_QUERY_ARGS}

        See :py:class:`ShapeFilter` for details about how the shape_filter
        parameter can be used.

        .. Note::
            Sensor shapes are not included in the result (In
            :py:meth:`Space.point_query` they are)

        Result:
            The resulting point query.
        """
        info = ffi.new("cpPointQueryInfo *")
        ptr = lib.cpSpacePointQueryNearest(
            self._cffi_ref, point, distance, filter, info
        )
        shape = shape_from_cffi(ptr)
        if shape:
            pos = Vec2d(info.point.x, info.point.y)
            grad = Vec2d(info.gradient.x, info.gradient.y)
            return PointQueryInfo(shape, pos, info.distance, grad)
        return None

    # noinspection PyShadowingBuiltins
    def segment_query(
        self,
        start: VecLike,
        end: VecLike,
        radius: float = 0.0,
        filter: ShapeFilter = FILTER_ALL,
    ) -> List[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        Args:
            start: Starting point
            end: End point
            radius: Radius
            filter: Shape filter

        Note:
            Sensor shapes are included in the result (In
            :py:meth:`Space.segment_query_first` they are not)
        """

        @ffi.callback("cpSpaceSegmentQueryFunc")
        def cb(ptr, point, normal, alpha, _data):
            shape = shape_from_cffi(ptr)
            if shape:
                pt = Vec2d(point.x, point.y)
                normal = Vec2d(normal.x, normal.y)
                query_hits.append(SegmentQueryInfo(shape, pt, normal, alpha))

        query_hits: List[SegmentQueryInfo] = []
        data = ffi.new_handle(self)
        lib.cpSpaceSegmentQuery(self._cffi_ref, start, end, radius, filter, cb, data)
        return query_hits

    # noinspection PyShadowingBuiltins
    def segment_query_first(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        radius: float = 0.0,
        filter: ShapeFilter = FILTER_ALL,
    ) -> Optional[SegmentQueryInfo]:
        """Query space along the line segment from start to end with the
        given radius.

        Similar to :py:meth:`Space.segment_query`, but return the first query
        or None.
        """

        info = ffi.new("cpSegmentQueryInfo *")
        filter = filter or ShapeFilter()
        ptr = lib.cpSpaceSegmentQueryFirst(
            self._cffi_ref, start, end, radius, filter, info
        )
        shape = shape_from_cffi(ptr)
        if shape is not None:
            pos = Vec2d(info.point.x, info.point.y)
            normal = Vec2d(info.normal.x, info.normal.y)
            return SegmentQueryInfo(shape, pos, normal, info.alpha)
        return None

    # noinspection PyShadowingBuiltins
    def bb_query(self, bb: "BB", filter: ShapeFilter = FILTER_ALL) -> List[Shape]:
        """Query space to find all shapes near bb.

        The filter is applied to the query and follows the same rules as the
        collision detection.

        Note:
            Sensor shapes are included in the result
        """

        @ffi.callback("cpSpaceBBQueryFunc")
        def cb(ptr, _):
            shape = shape_from_cffi(ptr)
            if shape:
                query_hits.append(shape)

        query_hits: List[Shape] = []
        data = ffi.new_handle(self)
        lib.cpSpaceBBQuery(self._cffi_ref, bb, filter, cb, data)
        return query_hits

    def shape_query(self, shape: Shape) -> List[ShapeQueryInfo]:
        """Query a space for any shapes overlapping the given shape

        Note:
            Sensor shapes are included in the result
        """

        @ffi.callback("cpSpaceShapeQueryFunc")
        def cb(ptr, points, _):
            shape = shape_from_cffi(ptr)
            if shape:
                point_set = contact_point_set_from_cffi(points)
                query_hits.append(ShapeQueryInfo(shape, point_set))

        query_hits: List[ShapeQueryInfo] = []
        data = ffi.new_handle(self)
        lib.cpSpaceShapeQuery(self._cffi_ref, shape._cffi_ref, cb, data)
        return query_hits

    def debug_draw(self: ST, options: Union["DrawOptions", str, None] = None) -> ST:
        """Draw the current state of the space using the supplied drawing
        options.

        If you use a graphics backend that is already supported, such as pygame
        and pyglet, you can use the predefined options their integration modules,
        for example :py:class:`pygame.DrawOptions`.

        Its also possible to write your own graphics backend, see
        :py:class:`SpaceDebugDrawOptions`.

        If you require any advanced or optimized drawing its probably best to
        not use this function for the drawing since its meant for debugging
        and quick scripting.

        Args:
            options: :py:class:`SpaceDebugDrawOptions`
        """

        if options is None:
            options = self.draw_options
        if options is None or isinstance(options, str):
            options = get_drawing_options(options)

        if options.bypass_chipmunk:
            options.draw_space(self)
            options.finalize_frame()
        else:
            # We need to hold ptr until the end of cpSpaceDebugDraw to prevent GC
            cffi = options._cffi_ref
            # noinspection PyUnusedLocal
            cffi.data = ptr = ffi.new_handle(self)  # noqa: F841
            with options:
                lib.cpSpaceDebugDraw(self._cffi_ref, cffi)
            del ptr
            options.finalize_frame()
        return self

    def draw(self: ST, options: "DrawOptions" = None) -> ST:
        """
        Draw space using the supplied drawing options.
        """
        options.draw_space(self)
        return self


@sk.curry(2)
def cffi_free_space(free_cb, cp_space):
    logging.debug("spacefree start %s", cp_space)
    cp_shapes = []
    cp_constraints = []
    cp_bodies = []

    @ffi.callback("cpSpaceShapeIteratorFunc")
    def cf1(shape, _):
        cp_shapes.append(shape)

    @ffi.callback("cpSpaceConstraintIteratorFunc")
    def cf2(constraint, _):
        cp_constraints.append(constraint)

    @ffi.callback("cpSpaceBodyIteratorFunc")
    def cf3(body, _):
        cp_bodies.append(body)

    lib.cpSpaceEachShape(cp_space, cf1, ffi.NULL)
    for cp_shape in cp_shapes:
        logging.debug("free %s %s", cp_space, cp_shape)
        lib.cpSpaceRemoveShape(cp_space, cp_shape)
        lib.cpShapeSetBody(cp_shape, ffi.NULL)

    lib.cpSpaceEachConstraint(cp_space, cf2, ffi.NULL)
    for cp_constraint in cp_constraints:
        logging.debug("free %s %s", cp_space, cp_constraint)
        lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)

    lib.cpSpaceEachBody(cp_space, cf3, ffi.NULL)
    for cp_body in cp_bodies:
        logging.debug("free %s %s", cp_space, cp_body)
        lib.cpSpaceRemoveBody(cp_space, cp_body)

    logging.debug("spacefree free %s", cp_space)
    free_cb(cp_space)
