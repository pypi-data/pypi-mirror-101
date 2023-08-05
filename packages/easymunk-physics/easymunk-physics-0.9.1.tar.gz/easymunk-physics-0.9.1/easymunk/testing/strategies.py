from collections import ChainMap

from hypothesis import strategies as st

from ..linalg import Vec2d

STRATEGY_MAP = {}
STRESS_STRATEGY_MAP = ChainMap({}, STRATEGY_MAP)


def reals(**kwargs):
    """
    Valid non-nan and non-infinity numeric values.

    It also avoid super-large values in order to minimize truncation errors.
    """
    kwargs.setdefault("width", 16)
    return st.floats(allow_nan=False, allow_infinity=False, **kwargs)


def angles(positive=False, max=360):
    """
    Return a angle in the range -360, 360.
    """
    start = 0 if positive else -max
    return st.floats(start, max, width=16)


def vecs(zero=True, like=False, **kwargs):
    """
    Nice Vec2d instances.

    Use st.builds(Vec2d) to create arbitrary vectors with nan and inf components.

    Args:
        zero:
            Set to false to forbid null vectors.
        like:
            Set to true to return generic VecLikes instead of Vec2d instances.
    """
    out = st.builds(Vec2d, reals(**kwargs), reals(**kwargs))
    if not zero:
        out = out.filter(lambda v: not (v.x == v.y == 0))
    if like:
        out = st.one_of(out, st.builds(tuple, out))
    return out


def strategy_from_prop(obj, prop):
    try:
        return st.from_type(obj.__annotations__[prop])
    except KeyError:
        return st.from_type(type(getattr(obj, prop)))
