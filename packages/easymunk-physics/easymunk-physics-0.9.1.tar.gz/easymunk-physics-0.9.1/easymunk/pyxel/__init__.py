"""
This submodule contains helper functions to help with quick prototyping
using easymunk together with pyxel.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated
about your coordinate system and not very optimized (they use batched
drawing, but there is probably room for optimizations still).
"""
# flake8: noqa
from .utils import arrow, arrowp, arrowr, get_pyxel

pyxel = get_pyxel()

from .draw_options import DrawOptions, Color, bg, fg, draw, drawb
from .bodies import (
    circ,
    tri,
    rect,
    line,
    poly,
    space,
    margin,
    moment_multiplier,
    reset_space,
)
from .camera import echo, Camera

__all__ = [k for k in globals() if not k.startswith("_")]
