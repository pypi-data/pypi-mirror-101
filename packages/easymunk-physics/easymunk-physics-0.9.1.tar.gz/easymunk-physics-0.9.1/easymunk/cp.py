"""
Utility functions for low level operation of Chipmunk CFFI.
"""
import re
from typing import Protocol, Generic, TypeVar, Any, overload

import _cffi_backend  # for PyInstaller, py2exe and other bundlers

try:
    from ._chipmunk import ffi, lib  # type: ignore
except ImportError:
    from pymunk._chipmunk import ffi, lib

from .linalg import Vec2d
from .typing import VecLike

T = TypeVar("T")
METHOD = re.compile(r"(\w+)\((\w+(?:\|\w+)*)\)?(\w+)?")

ffi = ffi
lib = lib
backend = _cffi_backend


class CWrapper(Protocol):
    """
    Declares objects that wraps chipmunk CData.
    """

    _cffi_ref: ffi.CData


class TypedDescriptor(Generic[T]):
    """
    A typed descriptor interface.

    It exists solely to help static analysis to infer the right types.
    """

    _value: T

    @overload
    def __get__(self, obj: None, typ=None) -> "cp_property":
        ...

    @overload
    def __get__(self, obj: Any, typ=None) -> T:
        ...

    def __get__(self, obj, typ=None):
        return self if obj is None else self._value

    def __set__(self, obj, value: T) -> None:
        ...


del TypedDescriptor.__get__, TypedDescriptor.__set__


class typed_property(TypedDescriptor[T], property):
    """
    A typed property.
    """


class cp_property(TypedDescriptor[T]):
    """
    A pseudo-descriptor that maps to Chipmunk C-API functions to properties.

    It builds regular properties, rather than cp_property instances. It is
    implemented in a way that tricks static analysis to assign the right
    types to the derived properties.
    """

    def __new__(cls, api: str, fset=None, doc: str = None, **kwargs):
        if not (m := METHOD.fullmatch(api)):
            raise ValueError(f"invalid API method name: {api!r}")

        prefix, opts, suffix = m.groups()
        methods = [getattr(lib, prefix + opt + suffix) for opt in opts.split("|")]

        fget, fset_, fdel = cls._from_methods(*methods, **kwargs)
        return property(fget, fset or fset_, fdel)

    @classmethod
    def _from_methods(
        cls, getter, setter=None, deleter=None, wrap=None, prepare=None
    ) -> tuple:
        fset = fdel = None  # type: ignore

        assert callable(getter)
        if wrap:
            assert callable(wrap)
            fget = lambda self: wrap(getter(self._cffi_ref))
        else:
            fget = lambda self: getter(self._cffi_ref)

        if setter and prepare:
            assert callable(setter)
            assert callable(prepare)
            fset = lambda self, value: setter(self._cffi_ref, prepare(value))
        elif setter:
            assert callable(setter)
            fset = lambda self, value: setter(self._cffi_ref, value)

        if deleter:

            def fdel(self):
                return deleter(self._cffi_ref)

        return fget, fset, fdel


class cpvec_property(cp_property[Vec2d]):
    """
    A cp_property that wraps vectors.
    """

    def __set__(self, obj, value: VecLike) -> None:
        ...

    @classmethod
    def _from_methods(cls, getter, setter=None, deleter=None, **kwargs) -> tuple:
        fset = fdel = None  # type: ignore

        def fget(self) -> Vec2d:
            v = getter(self._cffi_ref)
            return Vec2d(v.x, v.y)

        if setter:

            def fset(self, value: VecLike) -> None:
                return setter(self._cffi_ref, value)

        if deleter:

            def fdel(self, value: Any) -> None:
                return deleter(self._cffi_ref)

        return fget, fset, fdel
