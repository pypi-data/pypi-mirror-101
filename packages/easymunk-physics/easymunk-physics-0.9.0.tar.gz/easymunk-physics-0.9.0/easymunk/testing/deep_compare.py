from functools import singledispatch
from itertools import chain

from ..core import Space, Body
from ..abc import CpCFFIBase


def deep_compare(x, y, path=(), memo=None):
    """
    Conducts a deep search in x and y properties to verify if they are equal.

    Raise AssertionError, if not.
    """
    assert type(x) is type(y), (*path, f"bad types: {x}, {y}")
    key = (id(x), id(y))
    if memo is None:
        _compare(x, y, path, {key})
    elif key not in memo:
        memo.add(key)
        _compare(x, y, path, memo)


@singledispatch
def _compare(x, y, path, memo):
    raise TypeError(type(x))


def _compare_generic(x, y, path, memo):
    try:
        d1 = x.__dict__
        d2 = y.__dict__
    except AttributeError:
        raise TypeError(f"type not supported: {type(x).__name__}")

    deep_compare(d1, d2, path, memo)


for tt in (int, float, str, bytes, type(...), type(None)):

    @_compare.register(tt)
    def _(x, y, path, memo):
        assert x == y, (*path, f"not equal: {x} != {y}")


for tt in (list, tuple):

    @_compare.register(tt)
    def _(xs, ys, path, memo):
        assert (n := len(xs)) == (n_ := len(ys)), (*path, f"different sizes: {n}, {n_}")
        for i, x, y in zip(range(n), xs, ys):
            deep_compare(x, y, (*path, i), memo)


for tt in (set, frozenset):

    @_compare.register(tt)
    def _(xs, ys, path, memo):
        _compare(sorted(xs, key=hash), sorted(ys, key=hash), path, memo)


@_compare.register(dict)
def _(xs, ys, path, memo):
    _compare(set(xs.items()), set(ys.items()), path, memo)


@_compare.register
def _base_compare(x: CpCFFIBase, y, path, memo):
    for k in chain(x._pickle_args, x._pickle_kwargs):
        a = getattr(x, k)
        b = getattr(y, k)
        deep_compare(a, b, (*path, k), memo)

    for k, a in x.__dict__.items():
        if k not in x._pickle_meta_hide:
            b = getattr(y, k)
            deep_compare(a, b, (*path, k), memo)


@_compare.register
def _(x: Space, y, path, memo):
    _base_compare(x, y, path, memo)
    deep_compare(set(x.bodies), set(y.bodies), memo)
    deep_compare(set(x._junctions), set(y._junctions), memo)


@_compare.register
def _(x: Body, y, path, memo):
    _base_compare(x, y, path, memo)
    deep_compare(set(x.shapes), set(y.shapes), memo)
