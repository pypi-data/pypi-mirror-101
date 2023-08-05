from typing import (
    TypeVar,
    Callable,
    TYPE_CHECKING,
    Optional,
    Any,
    Type,
)

from .cp import ffi

if TYPE_CHECKING:
    from .core import Body

X, Y = 0, 1
T = TypeVar("T")


def void(_) -> None:
    """Explicitly *do not* return a value. This is used to make the
    type checker happy.
    """


def set_attrs(obj: T, **kwargs) -> T:
    """
    Set all given named attributes to object.
    """
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


def init_attributes(obj: Any, valid: set, values: dict) -> None:
    """
    Initialize attributes from dictionary, first verifying if attributes are
    present in a valid set.
    """
    if not valid.issuperset(values):
        invalid = set(values) - valid
        raise TypeError(f"invalid parameters: {invalid}")
    for k, v in values.items():
        setattr(obj, k, v)


#
# Normalize and fetch objects
#
def cffi_body(body: Optional["Body"]):
    """
    Return the C reference to body or a null pointer if body is None.
    """
    # noinspection PyProtectedMember
    return ffi.NULL if body is None else body._cffi_ref


def typed(_: Type[T]) -> Callable[[T], T]:
    """
    Explicitly type function with decorator.
    """

    def decorator(fn: T) -> T:
        return fn

    return decorator
