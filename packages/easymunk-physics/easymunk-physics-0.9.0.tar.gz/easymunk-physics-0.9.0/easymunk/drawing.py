import math
from functools import lru_cache
from math import degrees
from types import TracebackType
from typing import NamedTuple, Optional, Sequence, Tuple, Type, Any, TYPE_CHECKING

import sidekick.api as sk

from .cp import ffi, lib
from .linalg import Transform, Vec2d

if TYPE_CHECKING:
    from .types import BB
    from .core import (
        Body,
        Shape,
        Circle,
        Segment,
        Poly,
        Space,
    )

_DrawFlags = int


class Color(NamedTuple):
    """Color tuple used by the debug drawing API."""

    r: float
    g: float
    b: float
    a: float = 255

    def __repr__(self):
        return f"Color({self.r:n}, {self.g:n}, {self.b:n}, {self.a:n})"

    def as_int(self) -> Tuple[int, int, int, int]:
        """Return the color as a tuple of ints, where each value is rounded.

        >>> Color(0, 51.1, 101.9, 255).as_int()
        (0, 51, 102, 255)
        """
        return round(self[0]), round(self[1]), round(self[2]), round(self[3])

    def as_float(self) -> Tuple[float, float, float, float]:
        """Return the color as a tuple of floats, each value divided by 255.

        >>> Color(0, 51, 102, 255).as_float()
        (0.0, 0.2, 0.4, 1.0)
        """
        return self[0] / 255.0, self[1] / 255.0, self[2] / 255.0, self[3] / 255.0


class DrawOptions:
    """
    Configures debug drawing.

    If appropriate its usually easy to use the supplied draw implementations
    directly: easymunk.pygame_util, easymunk.pyglet_util and easymunk.matplotlib_util.
    """

    DRAW_SHAPES = lib.CP_SPACE_DEBUG_DRAW_SHAPES
    """Draw shapes.
    
    Use on the flags property to control if shapes should be drawn or not.
    """

    DRAW_CONSTRAINTS = lib.CP_SPACE_DEBUG_DRAW_CONSTRAINTS
    """Draw constraints.

    Use on the flags property to control if constraints should be drawn or not.
    """

    DRAW_COLLISION_POINTS = lib.CP_SPACE_DEBUG_DRAW_COLLISION_POINTS
    """Draw collision points.

    Use on the flags property to control if collision points should be drawn or
    not.
    """
    _COLOR = Color(255, 0, 0, 255)
    shape_dynamic_color = Color(52, 152, 219, 255)
    shape_static_color = Color(149, 165, 166, 255)
    shape_kinematic_color = Color(39, 174, 96, 255)
    shape_sleeping_color = Color(114, 148, 168, 255)
    shape_outline_color: Color
    shape_outline_color = property(  # type: ignore
        lambda self: self._cffi_to_color(self._cffi_ref.shapeOutlineColor),
        lambda self, c: setattr(self._cffi_ref, "shapeOutlineColor", c),
        doc="""The outline color of shapes.

        Should be a tuple of 4 ints between 0 and 255 (r, g, b, a).
        """,
    )
    constraint_color: Color
    constraint_color = property(  # type: ignore
        lambda self: self._cffi_to_color(self._cffi_ref.constraintColor),
        lambda self, c: setattr(self._cffi_ref, "constraintColor", c),
        doc="""The color of constraints.

        Should be a tuple of 4 ints between 0 and 255 (r, g, b, a).
        """,
    )
    collision_point_color: Color
    collision_point_color = property(  # type: ignore
        lambda self: self._cffi_to_color(self._cffi_ref.collisionPointColor),
        lambda self, c: setattr(self._cffi_ref, "collisionPointColor", c),
        doc="""The color of collisions.

        Should be a tuple of 4 ints between 0 and 255 (r, g, b, a).
        """,
    )
    flags: _DrawFlags
    flags = property(  # type: ignore
        lambda self: self._cffi_ref.flags,
        lambda self, f: setattr(self._cffi_ref, "flags", f),
        doc="""Bit flags which of shapes, joints and collisions should be drawn.
    
        By default all 3 flags are set, meaning shapes, joints and collisions 
        will be drawn.

        Example using the basic text only DebugDraw implementation (normally
        you would the desired backend instead, such as 
        `pygame_util.DrawOptions` or `pyglet_util.DrawOptions`):
        """,
    )

    def __init__(self, bypass_chipmunk=False, transform: Transform = None) -> None:
        ptr = ffi.new("cpSpaceDebugDrawOptions *")
        self._cffi_ref = ptr
        self.transform = transform
        self.shape_outline_color = Color(44, 62, 80, 255)
        self.constraint_color = Color(142, 68, 173, 255)
        self.collision_point_color = Color(231, 76, 60, 255)

        # Set to false to bypass chipmunk shape drawing code
        self.bypass_chipmunk = bypass_chipmunk
        self.flags = (
            DrawOptions.DRAW_SHAPES
            | DrawOptions.DRAW_CONSTRAINTS
            | DrawOptions.DRAW_COLLISION_POINTS
        )
        self._callbacks = cffi_register_debug_draw_options_callbacks(self, ptr)

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        typ: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional["TracebackType"],
    ) -> None:
        pass

    def _cffi_to_color(self, color: ffi.CData) -> Color:
        return Color(color.r, color.g, color.b, color.a)

    def _color_for_shape(self, color: Any):
        return Color(*color)

    def _print(self, *args, **kwargs):
        return print(*args, **kwargs)

    #
    # Drawing primitives
    #
    def draw_circle(
        self,
        pos: Vec2d,
        radius: float,
        angle: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        """
        Draw circle from position, radius, angle, and colors.
        """
        self._print("draw_circle", (pos, angle, radius, outline_color, fill_color))

    def draw_segment(self, a: Vec2d, b: Vec2d, color: Color = _COLOR) -> None:
        """
        Draw simple thin segment.
        """
        self._print("draw_segment", (a, b, color))

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        """
        Draw fat segment/capsule.
        """
        self._print("draw_fat_segment", (a, b, radius, outline_color, fill_color))

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        """
        Draw polygon from list of vertices.
        """
        self._print("draw_polygon", (verts, radius, outline_color, fill_color))

    def draw_dot(self, size: float, pos: Vec2d, color: Color) -> None:
        """
        Draw a dot/point.
        """
        self._print("draw_dot", (size, pos, color))

    #
    # Derived functions
    #
    def draw_shape(self, shape: "Shape") -> None:
        """
        Draw shape using other drawing primitives.
        """
        if shape.is_circle:
            shape: "Circle"
            self.draw_circle_shape(shape)
        elif shape.is_segment:
            shape: "Segment"
            self.draw_segment_shape(shape)
        elif shape.is_poly:
            shape: "Poly"
            self.draw_poly_shape(shape)
        else:
            raise ValueError(f"invalid shape: {shape}")

    def draw_circle_shape(self, circle: "Circle") -> None:
        """
        Default implementation that draws a circular shape.

        This function is not affected by overriding the draw method of shape.
        """
        kwargs = {
            "outline_color": self.shape_outline_color,
            "fill_color": self.color_for_shape(circle),
        }
        angle = circle.body.angle
        if (transform := self.transform) is None:
            self.draw_circle(circle.offset_world, circle.radius, angle, **kwargs)
        else:
            radius = transform.transform_scale(circle.radius)
            offset = transform.transform(circle.offset_world)
            self.draw_circle(offset, radius, angle, **kwargs)

    def draw_segment_shape(self, shape: "Segment") -> None:
        """
        Default implementation that draws a segment shape.

        This function is not affected by overriding the draw method of shape.
        """
        kwargs = {
            "outline_color": self.shape_outline_color,
            "fill_color": self.color_for_shape(shape),
        }
        if (transform := self.transform) is None:
            self.draw_fat_segment(shape.a_world, shape.b_world, shape.radius, **kwargs)
        else:
            radius = transform.transform_scale(shape.radius)
            a, b = transform.transform_path(shape.endpoints_world)
            self.draw_fat_segment(a, b, radius, **kwargs)

    def draw_poly_shape(self, shape: "Poly") -> None:
        """
        Default implementation that draws a polygonal shape.

        This function is not affected by overriding the draw method of shape.
        """
        kwargs = {
            "outline_color": self.shape_outline_color,
            "fill_color": self.color_for_shape(shape),
        }
        if (transform := self.transform) is None:
            self.draw_polygon(shape.get_vertices(world=True), shape.radius, **kwargs)
        else:
            radius = transform.transform_scale(shape.radius)
            vertices = transform.transform_path(shape.get_vertices(world=True))
            self.draw_polygon(vertices, radius, **kwargs)

    def draw_body(self, body: "Body") -> None:
        """
        Draw body from its shapes.
        """
        for shape in body.shapes:
            self.draw_shape(shape)

    def draw_space(self, space: "Space") -> None:
        """
        Draw space.
        """
        for body in space.bodies:
            self.draw_body(body)

    def draw_bb(self, bb: "BB") -> None:
        """
        Draw bounding box.
        """
        a, bs = sk.uncons(bb.vertices)
        for b in sk.concat(bs, [a]):
            self.draw_segment(a, b, self.shape_outline_color)
            a = b

    def draw_vec2d(self, vec: Vec2d):
        """
        Draw point from vector.
        """
        self.draw_dot(1, vec, self.shape_outline_color)

    def draw_object(self, obj):
        """
        Draw Easymunk object.
        """

        if isinstance(obj, Space):
            obj.debug_draw(self)
        elif isinstance(obj, Shape):
            self.draw_shape(obj)
        elif isinstance(obj, Body):
            for shape in obj.shapes:
                self.draw_shape(shape)
        else:
            raise TypeError(f"invalid type: {type(obj).__name__}")

    def color_for_shape(self, shape: "Shape") -> Color:
        if hasattr(shape, "color"):
            return self._color_for_shape(shape.color)  # type: ignore

        color = self.shape_dynamic_color
        if shape.body is not None:
            if shape.body.body_type == lib.CP_BODY_TYPE_STATIC:
                color = self.shape_static_color
            elif shape.body.body_type == lib.CP_BODY_TYPE_KINEMATIC:
                color = self.shape_kinematic_color
            elif shape.body.is_sleeping:
                color = self.shape_sleeping_color

        return color

    def finalize_frame(self):
        """
        Executed after debug-draw. The default implementation is a NO-OP.
        """


def color_from_cffi(color: ffi.CData) -> Color:
    return Color(color.r, color.g, color.b, color.a)


def cffi_register_debug_draw_options_callbacks(opts: DrawOptions, ptr):
    from .core.shapes import shape_from_cffi

    @ffi.callback("cpSpaceDebugDrawCircleImpl")
    def f1(pos, angle, radius, outline, fill, _):
        pos = Vec2d(pos.x, pos.y)
        c1 = color_from_cffi(outline)
        c2 = color_from_cffi(fill)
        opts.draw_circle(pos, radius, degrees(angle), c1, c2)

    @ffi.callback("cpSpaceDebugDrawSegmentImpl")
    def f2(a, b, color, _):  # type: ignore
        # sometimes a and/or b can be nan. For example if both endpoints
        # of a spring is at the same position. In those cases skip calling
        # the drawing method.
        if math.isnan(a.x) or math.isnan(a.y) or math.isnan(b.x) or math.isnan(b.y):
            return
        opts.draw_segment(Vec2d(a.x, a.y), Vec2d(b.x, b.y), color_from_cffi(color))

    @ffi.callback("cpSpaceDebugDrawFatSegmentImpl")
    def f3(a, b, radius, outline, fill, _):
        a = Vec2d(a.x, a.y)
        b = Vec2d(b.x, b.y)
        c1 = color_from_cffi(outline)
        c2 = color_from_cffi(fill)
        opts.draw_fat_segment(a, b, radius, c1, c2)

    @ffi.callback("cpSpaceDebugDrawPolygonImpl")
    def f4(count, verts, radius, outline, fill, _):
        vs = []
        for i in range(count):
            vs.append(Vec2d(verts[i].x, verts[i].y))
        opts.draw_polygon(vs, radius, color_from_cffi(outline), color_from_cffi(fill))

    @ffi.callback("cpSpaceDebugDrawDotImpl")
    def f5(size, pos, color, _):
        opts.draw_dot(size, Vec2d(pos.x, pos.y), color_from_cffi(color))

    @ffi.callback("cpSpaceDebugDrawColorForShapeImpl")
    def f6(shape, data):
        return opts.color_for_shape(shape_from_cffi(shape))

    ptr.drawCircle = f1
    ptr.drawSegment = f2
    ptr.drawFatSegment = f3
    ptr.drawPolygon = f4
    ptr.drawDot = f5
    ptr.colorForShape = f6

    return [f1, f2, f3, f4, f5, f6]


DEBUG_DRAW_PYGAME = sk.import_later(".pygame:DrawOptions", package=__package__)
DEBUG_DRAW_PYXEL = sk.import_later(".pyxel:DrawOptions", package=__package__)
DEBUG_DRAW_PYGLET = sk.import_later(".pyglet:DrawOptions", package=__package__)
DEBUG_DRAW_STREAMLIT = sk.import_later(".streamlit:DrawOptions", package=__package__)


@lru_cache
def get_drawing_options(opt) -> "DrawOptions":
    if opt is None:
        return get_drawing_options("pygame")
    elif opt == "pygame":
        return DEBUG_DRAW_PYGAME()
    elif opt == "pyglet":
        return DEBUG_DRAW_PYGLET()
    elif opt == "pyxel":
        return DEBUG_DRAW_PYXEL()
    elif opt == "streamlit":
        return DEBUG_DRAW_STREAMLIT()
    raise ValueError(f"invalid debug draw option: {opt}")
