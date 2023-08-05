import operator
from typing import (
    Sequence as Set,
    TypeVar,
    Dict,
    Callable,
    Any,
    Iterable,
    List,
    Iterator,
    TYPE_CHECKING, overload,
)
from itertools import chain
import sidekick.api as sk
from ..util import set_attrs
from ..cp import lib

if TYPE_CHECKING:
    from ..core import Body, Shape, Constraint

T = TypeVar("T")
T1 = TypeVar("T1")
OB = TypeVar("OB", bound="Objects")
Predicate = Callable[..., bool]

BODY_TYPES = {
    "dynamic": lib.CP_BODY_TYPE_DYNAMIC,
    "kinematic": lib.CP_BODY_TYPE_KINEMATIC,
    "static": lib.CP_BODY_TYPE_STATIC,
}


class Objects(Set[T]):
    """
    Collections of objects with richer APIs.

    Base class for the .shapes, .bodies, .constraints accessors.
    """

    _TAIL_MODIFIERS: Dict[str, Callable[[Any, Any], bool]] = {
        "gt": operator.gt,
        "ge": operator.ge,
        "lt": operator.lt,
        "le": operator.le,
        "eq": operator.eq,
        "ne": operator.ne,
        "len": lambda obj, n: len(obj) == n,
    }
    _CHAIN_MODIFIERS: Dict[str, Callable[[Any], Any]] = {
        "len": len,
    }

    def __init__(self, owner, objects):
        self.owner = owner
        self._objects: Callable[[], Iterator[T]] = objects

    def __repr__(self):
        return f"{type(self).__name__}({self._as_list()})"

    def __iter__(self):
        return self._objects()

    def __len__(self) -> int:
        return sum(1 for _ in self._objects())

    def __contains__(self, item):
        for obj in self._objects():
            if obj == item:
                return True
        return False

    @overload
    def __getitem__(self, i: int) -> T:
        ...

    @overload
    def __getitem__(self: OB, s: slice) -> OB:
        ...

    def __getitem__(self, i):
        if isinstance(i, int):
            for j, obj in enumerate(self._objects()):
                if i == j:
                    return obj
            raise IndexError(i)
        elif isinstance(i, slice):
            raise NotImplementedError
        else:
            raise TypeError(f"invalid index: {i}")

    def __eq__(self, other):
        if isinstance(other, list):
            return self._as_list() == other
        elif isinstance(other, set):
            return set(self._objects()) == other
        elif isinstance(other, Objects):
            if self._objects == other._objects:
                return True
            return set(self._objects()) == set(other._objects())
        return NotImplemented

    def _as_list(self):
        return list(self._objects())

    def _generic_filter_map(self, kwargs) -> Iterable[Predicate]:
        for k, v in kwargs.items():
            name, *mods = k.split("__")
            yield self._generic_filter(name, v, mods)

    # noinspection PyUnresolvedReferences
    def _generic_filter(self, name: str, value: Any, modifiers: List[str]) -> Predicate:
        """A Django-like filter query.

        It understands a simple DSL like in the example:

        >>> space.filter_objects(mass__gt=10)  # doctest: +SKIP
        ...
        """

        if not modifiers:
            return lambda o: getattr(o, name) == value

        if len(modifiers) == 1:
            mod_fn = self._tail_modifier(modifiers[0])
            return lambda o: mod_fn(o, value)

        *chain, tail = modifiers
        chain_fns = [*map(self._chain_modifier, chain)]
        tail_fn = self._tail_modifier(tail)

        def filter_with_modifiers(o):
            for fn in chain_fns:
                o = fn(o)
            return tail_fn(o, value)

        return filter_with_modifiers

    def _tail_modifier(self, name) -> Callable[[Any, Any], bool]:
        try:
            return self._TAIL_MODIFIERS[name]
        except KeyError:
            raise ValueError(f"invalid modifier: {name}")

    def _chain_modifier(self, name) -> Callable[[Any], Any]:
        try:
            return self._CHAIN_MODIFIERS[name]
        except KeyError:
            return operator.attrgetter(name)

    def get(self, *, first: bool = False, **kwargs) -> T:
        """
        Get single element from filter query. Raise ValueError if no element or
        if multiple values are found.

        This function accepts the same arguments as filter().
        If first=True, return the first match, even if multiple matches are
        found.
        """
        return single_query(self.filter(**kwargs), name="body", first=first)

    def filter(self: OB, **kwargs) -> OB:
        """
        Filter elements according to criteria.
        """
        # TODO: document filter eDSL
        filters = [*self._generic_filter_map(kwargs)]
        cls = type(self)
        return cls(self, lambda: filter(compose_filters(filters), self))

    def apply(self: OB, func: Callable[..., Any] = None, /, *args, **kwargs) -> OB:
        """Run func on each element of collection.

            ``func(elem, *args, **kwargs) -> None``

            Callback Parameters
                elem:
                    Each element in collection
                args:
                    Optional parameters passed to the callback function.
                kwargs:
                    Optional keyword parameters passed on to the callback function.

        The default function is :py:func:`set_attrs` and simply set attributes
        passed as keyword parameters.
        """
        if func is None:
            func = set_attrs
        for item in self:
            # noinspection PyArgumentList
            func(item, *args, **kwargs)
        return self

    def map(self, fn, *args, **kwargs) -> Iterator[Any]:
        """Map func on each element of collection returning an iterator.

        ``func(elem, *args, **kwargs) -> Any``

        Callback Parameters
            elem:
                Each element in collection
            args:
                Extra parameters passed to function.
            kwargs:
                Optional keyword parameters passed on to function.
        """
        if args or kwargs:
            return sk.map(lambda e: fn(e, *args, **kwargs), self)
        return sk.map(fn, self)


class Shapes(Objects["Shape"]):
    """
    Collection of shapes.
    """

    @property
    def circles(self):
        """
        Include only circles.
        """
        return self.filter(is_circle=True)

    @property
    def segments(self):
        """
        Include only segments.
        """
        return self.filter(is_segment=True)

    @property
    def polys(self):
        """
        Include only polys.
        """
        return self.filter(is_poly=True)

    @property
    def non_circles(self):
        """
        Include only all shapes that are not circles.
        """
        return self.filter(is_circle=False)

    @property
    def non_segments(self):
        """
        Include only all shapes that are not segments.
        """
        return self.filter(is_segment=False)

    @property
    def non_polys(self):
        """
        Include only all shapes that are not polys.
        """
        return self.filter(is_poly=False)


class Bodies(Objects["Body"]):
    """
    Collection of bodies.
    """

    @property
    def dynamic(self):
        """
        Include only dynamic bodies.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_DYNAMIC)

    @property
    def static(self):
        """
        Include only static bodies.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_STATIC)

    @property
    def kinematic(self):
        """
        Include only kinematic bodies.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_KINEMATIC)

    @property
    def non_dynamic(self):
        """
        Include all bodies that are not dynamic.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_DYNAMIC)

    @property
    def non_static(self):
        """
        Include all bodies that are not static.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_STATIC)

    @property
    def non_kinematic(self):
        """
        Include all bodies that are not kinematic.
        """
        return self.filter(body_type=lib.CP_BODY_TYPE_KINEMATIC)

    def _generic_filter_map(self, kwargs):
        filters = super()._generic_filter_map(kwargs)
        body_type = kwargs.pop("body_type", None)
        if body_type is not None:
            body_type = BODY_TYPES.get(body_type, body_type)
            return chain(filters, lambda b: b.body_type == body_type)
        return filters


class Constraints(Objects["Constraint"]):
    """
    Collection of constraints.
    """


def single_query(seq: Iterable[T], *, name: str = None, first=False):
    """
    Return first element of sequence and raise ValueError if sequence has more
    than one element.
    """
    seq = iter(seq)

    try:
        item = next(seq)
        if first:
            return item
    except StopIteration:
        raise ValueError("no element found")

    try:
        next(seq)
    except StopIteration:
        return item
    else:
        if name is None:
            name = type(item).__name__
        raise ValueError(f"more than one {name} was found!")


def compose_filters(filters: Iterable[Callable[..., bool]]) -> Callable[..., bool]:
    """
    Compose a sequence of filter functions.

    The resulting function returns True if all arguments also return True.
    """

    filters = tuple(filters)
    if not filters:
        return lambda *args: True
    elif len(filters) == 1:
        return filters[0]
    else:
        return lambda *args: all(fn(*args) for fn in filters)
