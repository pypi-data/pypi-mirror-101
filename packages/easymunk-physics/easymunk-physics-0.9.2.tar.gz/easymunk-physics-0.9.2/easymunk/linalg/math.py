"""
A clone of the math module, but trigonometric functions are based on degrees rather
than radians.
"""
# flake8: noqa
from contextlib import contextmanager
from math import *

_div = lambda x, y: x / y if y else copysign(x * y, float("inf"))
cos_radians, sin_radians, tan_radians = cos, sin, tan
acos_radians, asin_radians, atan_radians, atan_radians2 = acos, asin, atan, atan2
_COS_TABLE = {0: 1.0, 90: 0.0, 180: -1.0, 270: 0.0}
_SIN_TABLE = {(k + 90) % 360: v for k, v in _COS_TABLE.items()}
_TAN_TABLE = {k: _div(x, _COS_TABLE[k]) for k, x in _SIN_TABLE.items()}

cos = lambda x: cos_radians(radians(x))
sin = lambda x: sin_radians(radians(x))
tan = lambda x: tan_radians(radians(x))

acos = lambda x: degrees(acos_radians(x))
asin = lambda x: degrees(asin_radians(x))
atan = lambda x: degrees(atan_radians(x))
atan2 = lambda x, y: degrees(atan_radians2(x, y))


def sign(x) -> int:
    """Sign function.

    :return -1 if x < 0, else return 1
    """
    if x < 0:
        return -1
    else:
        return 1


# Slow implementation of trigonometric functions that return correct values for
# multiple of 90 angles.
#
# This is used on some tests.
def cos_stable(x) -> float:
    x %= 360
    return _COS_TABLE.get(x, cos(x))


def sin_stable(x) -> float:
    x %= 360
    return _SIN_TABLE.get(x, sin(x))


def tan_stable(x) -> float:
    x %= 360
    return _TAN_TABLE.get(x, tan(x))


@contextmanager
def patch_stable(mod, funcs=("cos", "sin", "tan")):
    """
    Patch module or object inside a with block replacing funcs with their
    stable versions.
    """

    empty = ()
    globs = globals()
    orig = [getattr(mod, k, empty) for k in funcs]

    for func in funcs:
        fn = globs[func + "_stable"]
        setattr(mod, func, fn)
    try:
        yield mod
    finally:
        for name, value in zip(funcs, orig):
            if value is empty:
                delattr(mod, name)
            else:
                setattr(mod, name, value)
