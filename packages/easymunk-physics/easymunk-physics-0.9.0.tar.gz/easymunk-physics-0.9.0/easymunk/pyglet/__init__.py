"""
This submodule contains helper functions to help with quick prototyping
using easymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated
about your coordinate system and not very optimized (they use batched
drawing, but there is probably room for optimizations still).
"""
__all__ = ["DrawOptions"]
from .draw_options import DrawOptions
