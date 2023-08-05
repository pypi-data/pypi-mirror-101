"""
Draw Pymunk elements using pyxel.
"""
import enum as _enum
from functools import singledispatch, lru_cache, partial
from typing import Optional

import pyxel

import sidekick.api as sk

from ..core import Body, Circle, Segment, Poly, Space
from ..drawing import Color as _Color, DrawOptions as DrawOptionsBase
from ..linalg import Vec2d


BACKGROUND_COLOR: Optional[int] = None
FOREGROUND_COLOR: int = pyxel.COLOR_WHITE


class Color(_enum.IntEnum):
    """
    Enum with Pyxel colors
    """

    BLACK = pyxel.COLOR_BLACK
    NAVY = pyxel.COLOR_NAVY
    PURPLE = pyxel.COLOR_PURPLE
    GREEN = pyxel.COLOR_GREEN
    BROWN = pyxel.COLOR_BROWN
    DARKBLUE = pyxel.COLOR_DARKBLUE
    LIGHTBLUE = pyxel.COLOR_LIGHTBLUE
    WHITE = pyxel.COLOR_WHITE
    RED = pyxel.COLOR_RED
    ORANGE = pyxel.COLOR_ORANGE
    YELLOW = pyxel.COLOR_YELLOW
    LIME = pyxel.COLOR_LIME
    CYAN = pyxel.COLOR_CYAN
    GRAY = pyxel.COLOR_GRAY
    PINK = pyxel.COLOR_PINK
    PEACH = pyxel.COLOR_PEACH


ALL_COLORS = [*Color]


class DrawOptions(DrawOptionsBase):
    _COLOR = Color

    @sk.lazy
    def palette(self):
        return [
            _Color(u // (256 * 256), u // 256 % 256, u % 256, 255)
            for u in pyxel.DEFAULT_PALETTE
        ]

    def __init__(self, mod=pyxel, keep_shape_colors=False, wireframe=False):
        self._line = mod.line
        self._circb = mod.circb
        self._circ = mod.circ
        self._pset = mod.pset
        self._draw_path = partial(draw_closed_path, mod=mod)
        self._draw_poly = partial(draw_filled_poly, mod=mod)
        self.keep_shape_colors = keep_shape_colors
        self.wireframe = wireframe
        color_map = {c: i for i, c in enumerate(self.palette)}

        @lru_cache(None)
        def to_color(color):
            if isinstance(color, int):
                return color
            try:
                return int(color_map[color])
            except KeyError:
                return int(color.r % 16)

        self._to_color = to_color
        self.shape_dynamic_color = self.palette[Color.WHITE]
        self.shape_static_color = self.palette[Color.DARKBLUE]
        self.shape_kinematic_color = self.palette[Color.CYAN]
        self.shape_sleeping_color = self.palette[Color.PEACH]
        super().__init__()

        self.shape_outline_color = self.palette[Color.GRAY]
        self.constraint_color = self.palette[Color.RED]
        self.collision_point_color = self.palette[Color.YELLOW]
        self.printed = False

    def _color_for_shape(self, color: int):
        return self.palette[color]

    def draw_circle(
        self, pos, radius, angle=0.0, outline_color=_COLOR, fill_color=_COLOR
    ):
        if self.wireframe:
            endpos = pos + Vec2d(radius, 0).rotated(angle)
            col = self._to_color(
                fill_color if self.keep_shape_colors else outline_color
            )
            self._circb(*pos, radius, col)
            self._line(*pos, *endpos, col)
        else:
            self._circ(*pos, radius, self._to_color(fill_color))

    def draw_segment(self, a, b, color=_COLOR):
        col = self._to_color(color)
        self._line(*a, *b, col)

    def draw_fat_segment(
        self, a, b, radius=0.0, outline_color=_COLOR, fill_color=_COLOR
    ):
        if self.wireframe:
            col = self._to_color(
                fill_color if self.keep_shape_colors else outline_color
            )
            self._line(*a, *b, self._to_color(col))
        elif radius <= 1:
            self._line(*a, *b, self._to_color(fill_color))
        else:
            self._circ(*a, radius, self._to_color(fill_color))
            self._circ(*b, radius, self._to_color(fill_color))
            side = radius * (b - a).perpendicular_normal()
            vs = [a + side, a - side, b - side, b + side]
            self.draw_polygon(vs, 0, outline_color, fill_color)

    def draw_polygon(self, verts, radius=0.0, outline_color=_COLOR, fill_color=_COLOR):
        if self.wireframe:
            col = self._to_color(
                fill_color if self.keep_shape_colors else outline_color
            )
            self._draw_path(verts, self._to_color(col))
        else:
            self._draw_poly(verts, self._to_color(fill_color))

    def draw_dot(self, size: float, pt, col):
        self._circ(*pt, int(size / 2), self._to_color(col))


#
# Background/foreground drawing
#
def bg(col=None) -> int:
    """
    Get or set the default background color for space objects.
    """
    global BACKGROUND_COLOR

    if col is None:
        return BACKGROUND_COLOR
    else:
        BACKGROUND_COLOR = int(col)
        return BACKGROUND_COLOR


def fg(col=None) -> int:
    """
    Get or set the default foreground color for space objects.
    """
    global FOREGROUND_COLOR

    if col is None:
        return FOREGROUND_COLOR
    else:
        FOREGROUND_COLOR = int(col)
        return FOREGROUND_COLOR


#
# Draw Pymunk shapes
#
@singledispatch
def draw(shape, col=None, mod=pyxel):
    """
    Draw Pymunk shape or all shapes in a Pymunk body or space with a given
    offset.

    Args:
        shape: A Pymunk shape, body or space
        mod: x coordinate offset
        col (int): A color index
    """
    try:
        method = shape.draw
    except AttributeError:
        name = type(shape).__name__
        raise TypeError(f"Cannot draw {name} objects")
    else:
        return method(mod, col=col)


@singledispatch
def drawb(shape, col=None, mod=pyxel):
    """
    Like draw, but renders only the outline of a shape.

    Args:
        shape: A Pymunk shape, body or space
        mod: mod namespace  that transforms the scene.
        col (int): A color index
    """
    try:
        method = shape.drawb
    except AttributeError:
        name = type(shape).__name__
        raise TypeError(f"Cannot draw {name} objects")
    else:
        return method(mod, col=col)


#
# Register implementation for draw() and drawb() functions
#
@draw.register(Space)
def draw_space(s: Space, col=None, mod=pyxel):
    if hasattr(s, "background_color"):
        pyxel.cls(s.background_color)
    elif BACKGROUND_COLOR is not None:
        pyxel.cls(BACKGROUND_COLOR)
    for b in s.bodies:
        draw(b, col, mod)


@draw.register(Body)
def draw_body(b: Body, col=None, mod=pyxel):
    if col is None:
        col = getattr(b, "color", None)
    for s in b.shapes:
        draw(s, col, mod)


@draw.register(Circle)
def draw_circle(s: Circle, col=None, mod=pyxel):
    if col is None:
        col = getattr(s, "color", FOREGROUND_COLOR)
    mod.circ(*(s.position + s.offset), s.radius, col)


@draw.register(Segment)
def draw_segment(s: Segment, col=None, mod=pyxel):
    (x1, y1), (x2, y2) = map(s.local_to_world, [s.a, s.b])
    if col is None:
        col = getattr(s, "color", FOREGROUND_COLOR)
    mod.line(x1, y1, x2, y2, col)


@draw.register(Poly)
def draw_poly(s: Poly, col=None, mod=pyxel):
    vertices = [s.local_to_world(v) for v in s.get_vertices()]
    if col is None:
        col = getattr(s, "color", FOREGROUND_COLOR)
    return draw_filled_poly(vertices, col, mod)


def draw_filled_poly(vertices, col=None, mod=pyxel):
    n = len(vertices)
    if n == 1:
        x, y = vertices[0]
        mod.pset(x, y, col)
        return
    elif n == 2:
        (x1, y1), (x2, y2) = vertices
        mod.line(x1, x2, y1, y2, col)
        return

    (x1, y1), (x2, y2), (x3, y3), *rest = vertices
    mod.tri(x1, y1, x2, y2, x3, y3, col)
    rest.reverse()

    while rest:
        x2, y2 = x3, y3
        x3, y3 = rest.pop()
        mod.tri(x1, y1, x2, y2, x3, y3, col)


def draw_path(path, col=None, mod=pyxel):
    a, *rest = path
    for b in path:
        mod.line(*a, *b, col)
        a = b


def draw_closed_path(path, col, mod=pyxel):
    draw_path(path, col, mod)
    mod.line(*path[0], *path[-1], col)


@drawb.register(Space)
def drawb_space(s: Space, col=None, mod=pyxel):
    if hasattr(s, "background_color"):
        pyxel.cls(s.background_color)
    elif BACKGROUND_COLOR is not None:
        pyxel.cls(BACKGROUND_COLOR)
    for b in s.bodies:
        drawb(b, col, mod)


@drawb.register(Body)
def drawb_body(b: Body, col=None, mod=pyxel):
    if col is None:
        col = getattr(b, "color", None)
    for s in b.shapes:
        drawb(s, col, mod)


@drawb.register(Circle)
def drawb_circle(s: Circle, col=None, mod=pyxel):
    if col is None:
        col = getattr(s, "color", FOREGROUND_COLOR)
    mod.circb(*s.offset_world, s.radius, col)


@drawb.register(Poly)
def drawb_poly(s: Poly, col=None, mod=pyxel):
    vertices = s.get_vertices(world=True)
    vertices.append(vertices[0])
    if col is None:
        col = getattr(s, "color", FOREGROUND_COLOR)
    return draw_path(vertices, col, mod)


drawb.register(Segment, draw_segment)
