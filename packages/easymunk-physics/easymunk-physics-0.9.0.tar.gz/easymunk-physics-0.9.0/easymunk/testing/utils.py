from functools import wraps
from typing import Sequence, Callable, Any, TypeVar, Iterable

import pytest
from hypothesis import strategies as st, given
from sidekick import op

from .strategies import strategy_from_prop

T = TypeVar("T")
S = TypeVar("S")
NOT_GIVEN = object()


#
# Testing functions
#
def test_mutable_property(
    obj: T,
    attr: str,
    values: Sequence[S] = NOT_GIVEN,
    normalize: bool = False,
    eq: Callable[[S, Any], bool] = op.eq,
    invariants: Sequence[Callable[[T, S], bool]] = (),
    silent: bool = False,
) -> None:
    """
    Check if object respects the "mutable attribute" interface. It assigns each of
    the given values to the selected attribute and verifies if the value is actually
    written.

    Args:
        obj:
            Target object.
        attr:
            Name of test attribute.
        values:
            If given, must be a sequence of values to test. If not given, it tries
            to compute values from type. It also accepts values as an hypothesis
            strategy object.
        normalize:
            If True, verify if resulting value is consistent with the desired
            type. Type is extracted from annotations
        invariants:
            A predicate function (obj, value) -> bool that verifies if assignment
            preserves some invariant property.
    """
    if not silent:
        print(f"testing property {attr} of {type(obj).__name__}")

    original = getattr(obj, attr, NOT_GIVEN)
    original_type = type(original)  # type = object(), if NOT_GIVEN. That is OK!
    values = _values_strategy(obj, attr, values)

    @given(values)
    def verify_attribute(v):
        try:
            u = verify_assign_and_read(obj, attr, v)

            # Verify equality
            if not eq(u, v):
                msg = f"After setting obj.{attr} = {v}, obj.{attr} was equal to {u}"
                raise AssertionError(msg)

            # Verify types
            if normalize and not isinstance(v, original_type):
                cls = original_type.__name__
                cls_ = type(u).__name__
                msg = f"resulting obj.{attr} is not an instance of {cls}, got {cls_}"
                raise AssertionError(msg)

            verify_invariants(obj, v, invariants)
        finally:
            if original is not NOT_GIVEN:
                setattr(obj, attr, original)

    verify_attribute()


def test_immutable_properties(obj, props=None):
    for attr in props:
        try:
            u = getattr(obj, attr)
            setattr(obj, attr, u)
        except AttributeError:
            ...


def _values_strategy(obj: Any, attr: str, values: Sequence = NOT_GIVEN):
    """
    Normalize a strategy to generate values.

    Values can be passed as a sequence of values, or inferred from attribute in
    object.
    """
    if values is NOT_GIVEN:
        return strategy_from_prop(obj, attr)
    else:
        return st.sampled_from(values)


def verify_assign_and_read(obj: Any, attr: str, value: Any) -> Any:
    """
    Assign value to attribute, read and return result.

    Assert that values can be mutated and read before and after mutation.
    """
    try:
        setattr(obj, attr, value)
    except AttributeError:
        raise AssertionError(f"error mutating obj.{attr}")

    try:
        return getattr(obj, attr)
    except AttributeError:
        raise AssertionError(f"obj.{attr} does not exist even after assignment")


def verify_invariants(obj: T, value: S, invariants: Iterable[Callable[[T, S], bool]]):
    """
    Verify if object obj respect all invariants given as functions
    f(obj, attr_value) -> bool that tests if some property of an attribute
    holds for object.
    """
    for i, invariant in enumerate(invariants):
        try:
            if invariant(obj, value):
                continue
            msg = "failed evaluating predicate!"
        except AssertionError as ex:
            msg = str(ex)

        name = getattr(invariant, "__name__")
        raise AssertionError(f"error evaluating invariants[{i}]={name}: {msg}")


#
# Pytest
#
def description_fixture(*args, **kwargs):
    """
    A fixture that adds the docstring to the .description attribute of its
    resulting value.
    """

    def decorator(fn):
        @pytest.fixture(*args, **kwargs)
        @wraps(fn)
        def decorated(*args_, **kwargs_):
            obj = fn(*args_, **kwargs_)
            doc = fn.__doc__ or ""
            descr = "\n".join(ln.strip() for ln in doc.strip().splitlines())
            obj.description = descr
            return obj

        return decorated

    return decorator
