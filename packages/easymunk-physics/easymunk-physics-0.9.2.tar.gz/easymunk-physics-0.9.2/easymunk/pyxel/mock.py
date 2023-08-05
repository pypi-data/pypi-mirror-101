"""
A mock Pyxel module. This is useful for testing.
"""
import io
import os
import warnings
from contextlib import contextmanager, redirect_stdout
from functools import lru_cache
from itertools import count
from typing import Any, Sequence, List, Set

from .utilities import echo_mod as _echo_mod

_BTN: Set[int] = set()

if os.environ.get("EASYMUNK_MOCK", "").lower() not in ("yes", "true"):
    warnings.warn(
        """
You need pyxel installed in your system. We are importing the mock module that
pretends to be Pyxel but just prints function calls to the the terminal. This is 
useful for testing and debugging, but it is obviously not very useful for writing
an actual game. 

Please ``pip install pyxel`` before loading this module."""
    )

#
# Constants
#
width = height = mouse_x = mouse_y = frame_count = 0
caption = scale = palette = fps = quit_key = fullscreen = None

# Colors
(
    COLOR_BLACK,
    COLOR_NAVY,
    COLOR_PURPLE,
    COLOR_GREEN,
    COLOR_BROWN,
    COLOR_DARKBLUE,
    COLOR_LIGHTBLUE,
    COLOR_WHITE,
    COLOR_RED,
    COLOR_ORANGE,
    COLOR_YELLOW,
    COLOR_LIME,
    COLOR_CYAN,
    COLOR_GRAY,
    COLOR_PINK,
    COLOR_PEACH,
) = range(16)


# Keys
@lru_cache(None)
def _assign_new_key_number(name: str):
    global KEY_INDEX

    KEY_INDEX += 1
    return KEY_INDEX


KEY_INDEX = 0


#
# User input
#
def btn(key):
    return key in _BTN


# TODO: mock btnp and btnr interactions
def btnp(key, hold: int = 0, period: int = 0):
    return False


def btnr(key):
    return False


#
# Other functions in Pyxel API
#
def init(
    width: int,
    height: int,
    *,
    caption: str = None,
    scale: int = None,
    palette: List[int] = None,
    fps: int = 30,
    quit_key: int = _assign_new_key_number("KEY_ESCAPE"),
    fullscreen: bool = False,
):
    globals().update(
        {
            "width": width,
            "height": height,
            "caption": caption,
            "scale": scale,
            "palette": palette,
            "fps": fps,
            "quit_key": quit_key,
            "fullscreen": fullscreen,
            "frame_count": 0,
            "mouse_x": width // 2,
            "mouse_y": height // 2,
        }
    )
    _BTN.clear()


def run(update, draw, max_iter=None, stop=lambda: False):
    if max_iter is None:
        max_iter = os.environ.get("PYXEL_MAX_ITER")

    frames = count() if max_iter is None else range(int(max_iter))
    for idx in frames:
        if stop():
            break
        print(f"\nframe: {idx}")
        advance_to_frame(update, draw, idx)


#
# Advance to frame
#
def advance_to_frame(update=lambda: None, draw=lambda: None, frame=0):
    """
    Advance to frame executing the update and draw functions.
    """
    global frame_count

    frame_count = frame
    update()
    draw()


#
# Utilities
#
@contextmanager
def patch(var: str, value: Any, ns=globals()):
    old = ns[var]
    ns[var] = value
    yield value
    ns[var] = old


@contextmanager
def set_mouse_pos(x: int, y: int):
    with patch("mouse_x", x), patch("mouse_y", y):
        yield


@contextmanager
def press_keys(*args):
    # Is it a good API?
    if len(args) == 1 and isinstance(args[0], Sequence):
        args = args[0]

    with patch("_BTN", set(args)):
        yield


@contextmanager
def set_screen(width: int, height: int):
    with patch("width", width), patch("height", height):
        yield


@contextmanager
def capture(file=None):
    if file is None:
        file = io.StringIO()

    with redirect_stdout(file) as fd:
        yield fd


@lru_cache(None)
def __getattr__(name):
    if name.startswith("KEY_"):
        return _assign_new_key_number(name)
    else:
        return getattr(_echo_mod, name)
