from abc import ABC
from functools import singledispatch
from typing import TypeVar, ClassVar, List, Set, Iterable, Tuple, Any, TYPE_CHECKING

from sidekick import api as sk

from .ipython_renderer import IPythonRenderer
from ..cp import ffi
from ..util import set_attrs

T = TypeVar("T", bound="CpCFFIBase")


class CpCFFIBase(ABC):
    """
    Base class for wrappers around Chipmunk's CFFI pointers.

    Provides pickling, copying, and basic memory management functionalities.
    """

    is_body = is_shape = is_space = is_constraint = False

    _pickle_args: ClassVar[List[str]] = []
    _pickle_kwargs: ClassVar[List[str]] = []
    _pickle_meta_hide: ClassVar[Set[str]] = set()
    _ipython_renderer = IPythonRenderer()

    # Keep references before adding objects to space
    _nursery: List["CpCFFIBase"]
    _nursery = sk.lazy(lambda self: [])  # type: ignore

    # CFFI
    _cffi_ref: ffi.CData

    def __getstate__(self):
        args = [getattr(self, k) for k in self._pickle_args]
        meta = dict(self.__dict__)
        for k in self._pickle_meta_hide:
            meta.pop(k, None)
        for k in self._pickle_kwargs:
            meta[k] = getattr(self, k)
        return args, meta

    def __setstate__(self, state):
        args, meta = state
        # noinspection PyArgumentList
        self.__init__(*args)  # type: ignore
        for k, v in meta.items():
            setattr(self, k, v)

    #
    # Include those functions to allow type checking to accept custom attributes
    #
    def __setattr__(self, name: str, value: Any) -> None:
        """Override default setattr to make sure type checking works."""
        super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Any:
        """Override default getattr to make sure type checking works."""
        return self.__getattribute__(name)

    if not TYPE_CHECKING:
        del __setattr__, __getattr__

    def _repr_html_(self):
        return self._ipython_renderer.html()

    def _repr_javascript_(self):
        return self._ipython_renderer.javascript()

    def _repr_svg_(self):
        return self._ipython_renderer.svg()

    def _repr_png_(self):
        return self._ipython_renderer.png()

    def _repr_jpeg_(self):
        return self._ipython_renderer.jpeg()

    def copy(self: T, **opts) -> T:
        """
        Return copy of object, possibly overriding some attributes passed as
        keyword arguments.
        """
        state = self.__getstate__()
        new = object.__new__(type(self))

        if not opts:
            new.__setstate__(state)
            return new

        args, kwargs = state
        keys = set(opts)
        for k in keys.intersection(kwargs):
            kwargs[k] = opts.pop(k)
            keys.remove(k)

        if keys:
            args = list(args)
            for i, k in enumerate(self._pickle_args):
                if k in keys:
                    args[i] = opts.pop(k)

        new.__setstate__((args, kwargs))
        return new

    def update(self: T, **kwargs) -> T:
        """
        Update attributes of object.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def apply(self: T, func=None, /, *args, **kwargs) -> T:
        """Apply function to object, passing additional positional and keyword
        arguments..

            ``func(elem, *args, **kwargs) -> None``

        The default function :py:func:`set_attrs` simply set attributes passed
        as keyword parameters.
        """
        if func is None:
            set_attrs(self, **kwargs)
        else:
            func(*args, **kwargs)
        return self

    def destroy(self: T) -> T:
        """
        Detach object from space and renders it unusable.
        """
        self.detach()
        self.__dict__.clear()
        self._cffi_ref = None
        return self

    def detach(self: T) -> T:
        raise NotImplementedError

    def describe(self, indent: str = "    ", name=None, description=None, memo=None):
        """
        Describe object.
        """
        if memo is None:
            memo = {self}
        lines = sk.concat(
            [
                self._describe_head(indent, name, description),
                self._describe_body(indent, memo),
                "}",
            ]
        )
        return "\n".join(lines)

    def _describe_head(self, indent: str, name: str, description: str) -> List[str]:
        cls = type(self).__name__
        if name := getattr(self, "name", None) or name or "":
            cls += f' "{name}"'
        yield cls + " {"

        if descr := (getattr(self, "description", "") or description or "").strip():
            for ln in descr.splitlines():
                yield indent + "# " + ln

    def _describe_objects(self, memo) -> Iterable[Tuple[str, Any]]:
        for arg in (*self._pickle_args, *self._pickle_kwargs):
            obj = getattr(self, arg)
            yield arg, obj

    def _describe_body(self, indent: str, memo):
        yield from self._describe_collection(self._describe_objects(memo), indent, memo)

    def _describe_element(self, name: str, obj, indent, memo) -> Iterable[str]:
        if isinstance(obj, (list, set, frozenset)) and len(obj) >= 1:
            yield f"{name}: {{"
            yield from self._describe_collection(enumerate(obj), indent + "    ", memo)
            yield "}"
        elif hasattr(obj, "describe"):
            if obj not in memo:
                yield obj.describe(indent + "    ")
                memo.add(obj)
        else:
            yield f"{name}: {_describe(obj)}"

    def _describe_collection(self, objs: Iterable, indent: str, memo) -> Iterable[str]:
        for name, obj in sorted(objs):
            for ln in self._describe_element(name, obj, indent, memo):
                yield indent + ln


@singledispatch
def _describe(obj):
    return repr(obj)


for cls in (int, float, complex):
    _describe.register(cls, lambda x: f"{x:n}")

_describe.register(tuple, lambda xs: "(" + ", ".join(map(_describe, xs)) + ")")
_describe.register(list, lambda xs: f"[{_describe(tuple(xs))}]")
_describe.register(set, lambda xs: f"[{_describe(tuple(xs))}]")
