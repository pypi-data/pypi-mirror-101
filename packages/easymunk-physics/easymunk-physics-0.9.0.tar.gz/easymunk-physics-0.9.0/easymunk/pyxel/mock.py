"""
A mock Pyxel module. This is useful for testing.
"""
import io
import os
import warnings
from contextlib import contextmanager, redirect_stdout
from functools import lru_cache
from typing import Any

from .camera import echo

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
width = height = mouse_x = mouse_y, frame_count = 0


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
    return False


def btnp(key, hold: int = 0, period: int = 0):
    return False


def btnr(key):
    return False


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
def set_screen(width: int, height: int):
    with patch("width", width), patch("height", height):
        yield


@contextmanager
def capture(file=None):
    if file is None:
        file = io.StringIO()

    with redirect_stdout(file) as fd:
        yield fd


def __getattr__(name):
    if name.startswith("KEY_"):
        return _assign_new_key_number(name)
    else:
        return getattr(echo, name)
