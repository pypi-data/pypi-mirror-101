from functools import partial, lru_cache
from typing import Dict
import sys

try:
    import pyxel
except ImportError:
    from . import mock as pyxel

from ..linalg import Vec2d

ARROW_KEYS_MAP: Dict[str, tuple] = {
    "arrows": (pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN),
    "adws": (pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_W, pyxel.KEY_S),
    "numpad": (pyxel.KEY_KP_4, pyxel.KEY_KP_6, pyxel.KEY_KP_8, pyxel.KEY_KP_2),
    "numpad5": (pyxel.KEY_KP_4, pyxel.KEY_KP_6, pyxel.KEY_KP_8, pyxel.KEY_KP_5),
}
ARROW_KEYS = ARROW_KEYS_MAP["arrows"]
ARROW_FN_DOC = """
    Return a vector of coordinates (x, y) from user input pressing the given
    set of [left, right, up, down] keys.

    Args:
        x: value of x coordinate of resulting vector.
        y: value of y coordinate of resulting vector.
        keys: List of keys, defaults to arrow keys. List of keys mapped to
            left, right, up, down actions. It also understands the following
            strings:
            * "adws": Conventional A, D, W, S mapping.
            * "arrows": Arrow keys
            * "numpad": Numpad arrow keys
            * "numpad5": Numpad arrow keys, with 5 acting as down.

        default: Default value if no key is pressed for the given axis.

    Returns:
        A vector (±x, ±y) depending on which keys are pressed.
"""


#
# User input helpers
#
def arrow(x: float, y: float, keys=ARROW_KEYS, default: float = 0.0) -> Vec2d:
    f"""
    {ARROW_FN_DOC}

    Note:
        It uses pyxel.btn() to check button presses.
    """
    return _arrows(pyxel.btn, x, y, keys, default)


def arrowp(
    x: float,
    y: float,
    hold: int = 0,
    period: int = 0,
    keys=ARROW_KEYS,
    default: float = 0.0,
) -> Vec2d:
    f"""
    {ARROW_FN_DOC}
    Note:
        It uses pyxel.btnp() to check button presses.
    """
    fn = partial(pyxel.btnp, hold=hold, period=period)
    return _arrows(fn, x, y, keys, default)


def arrowr(x: float, y: float, keys=ARROW_KEYS, default: float = 0.0) -> Vec2d:
    f"""
    {ARROW_FN_DOC}

    Note:
        It uses pyxel.btnr() to check button presses.
    """
    return _arrows(pyxel.btnr, x, y, keys, default)


def _arrows(fn, x, y, keys: tuple, default) -> Vec2d:
    """
    Implementation of arrow, arrowp and arrowr functions.
    """
    if isinstance(keys, str):
        try:
            keys = ARROW_KEYS_MAP[keys]
        except KeyError:
            keys = _get_keys(keys)

    if fn(keys[0]):
        x_coord = -x
    elif fn(keys[1]):
        x_coord = x
    else:
        x_coord = default

    if fn(keys[2]):
        y_coord = y
    elif fn(keys[3]):
        y_coord = -y
    else:
        y_coord = default

    return Vec2d(x_coord, y_coord)


@lru_cache(32)
def _get_keys(keys):
    try:
        if keys.isalpha() and len(keys) == 4:
            return [getattr(pyxel, f"KEY_{k.upper()}") for k in keys]
        raise KeyError
    except KeyError:
        raise ValueError(f"invalid sequence: {keys!r}")


def get_pyxel():
    """
    Return the loaded pyxel module.
    """
    sys.modules["pyxel"] = pyxel
    return pyxel
