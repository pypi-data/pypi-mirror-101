"""
Easier factory functions for creating Pymunk objects.
"""
from functools import wraps
from typing import Sequence, Union, Callable, TypeVar, TYPE_CHECKING

import pyxel
import sidekick.api as sk

from . import Color, DrawOptions
from ..core import CircleBody, SegmentBody, PolyBody, Body, Space
from ..typing import VecLike

if TYPE_CHECKING:
    from .camera import Camera

T = TypeVar("T")
ColorT = Union[Color, int]

DEFAULT_SPACE = None
DEFAULT_COLOR = None
MOMENT_MULTIPLIER = 5.0
DEFAULT_ELASTICITY = 0.0
DEFAULT_FRICTION = 0.0


@sk.curry(2)
def body_maker_function(col_arg, func):  # type: ignore
    """
    Decorate function that normalize input arguments and outputs for a pyxel
    context.
    """

    @wraps(func)
    def maker(*args, **kwargs):
        args = list(args)
        kwargs.setdefault("space", DEFAULT_SPACE)
        kwargs.setdefault("elasticity", DEFAULT_ELASTICITY)
        kwargs.setdefault("friction", DEFAULT_FRICTION)
        target_body = kwargs.pop("body", None)
        if len(args) > col_arg:
            color = args.pop(col_arg)
        elif "color" in kwargs:
            color = kwargs.pop("color")
        else:
            color = DEFAULT_COLOR

        body = func(*args, **kwargs)

        if "moment" not in kwargs:
            body.moment *= MOMENT_MULTIPLIER

        if color is not None:
            body.shapes.apply(color=color)
            body.color = color

        if target_body is not None:
            for shape in body.shapes:
                shape_ = shape.copy(body=target_body)
                if target_body.space:
                    target_body.space.add(shape_)
            body = target_body
        return body

    return maker


# We use this trick to convince static analysis of the right types while
# sidekick do not provide good types for Curried functions.
def body_maker(n: int) -> Callable[[T], T]:
    def decorator(fn: T) -> T:
        return body_maker_function(n, fn)  # type: ignore

    return decorator


#
# Basic geometric shapes
#
@body_maker(3)
def circ(x: float, y: float, r: float, col: int = None, **kwargs) -> CircleBody:
    """
    Creates a body with a Circle shape attached to it.

    Args:
        x: Center point x coordinate
        y: Center point y coordinate
        r: Circle radius
        col: Object's color
    """
    if col is not None:
        kwargs["color"] = col
    return CircleBody(r, position=(x, y), **kwargs)


@body_maker(4)
def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    col: int = None,
    radius: float = 1.0,
    **kwargs
) -> SegmentBody:
    """
    Creates a body with a Segment shape attached to it.

    Args:
        x1: x coordinate of starting point
        y1: y coordinate of starting point
        x2: x coordinate of ending point
        y2: y coordinate of ending point
        col: Object's color
        radius (float): Collision radius for line element.
    """
    if col is not None:
        kwargs["color"] = col
    return SegmentBody((x1, y1), (x2, y2), radius=radius, **kwargs)


@body_maker(6)
def tri(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    col: int = None,
    radius: float = 0.0,
    **kwargs
) -> PolyBody:
    """
    Creates a Pymunk body with a triangular Poly shape attached to it.

    Args:
        x1: x coordinate of first point
        y1: y coordinate of first point
        x2: x coordinate of second point
        y2: y coordinate of second point
        x3: x coordinate of last point
        y3: y coordinate of last point
        col: Object's color
        radius: Collision radius for line element.
    """
    if col is not None:
        kwargs["color"] = col
    return PolyBody([(x1, y1), (x2, y2), (x3, y3)], radius=radius, **kwargs)


@body_maker(4)
def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    col: int = None,
    radius: float = 0.0,
    **kwargs
) -> PolyBody:
    """
    Creates a Pymunk body with a triangular Poly shape attached to it.

    Args:
        x: x coordinate of starting point
        y: y coordinate of starting point
        w: width
        h: height
        col: Object's color
        radius: Collision radius for line element.
    """
    x_ = x + w / 2
    y_ = y + h / 2
    if col is not None:
        kwargs["color"] = col
    return PolyBody.new_box((w, h), position=(x_, y_), radius=radius, **kwargs)


@body_maker(1)
def poly(
    vs: Sequence[VecLike], col: int = None, radius: float = 0.0, **kwargs
) -> PolyBody:
    """
    Creates a Pymunk body with a polygonal shape attached to it.

    Args:
        vs: sequence of vertices.
        col: Object's color
        radius: collision radius tolerance.
    """
    if col is not None:
        kwargs["color"] = col
    return PolyBody(vs, radius=radius, **kwargs)


@body_maker(4)
def margin(
    x: float = 0,
    y: float = 0,
    width: float = None,
    height: float = None,
    col: int = None,
    **kwargs
) -> Body:
    """
    Creates a margin around the screen.
    """
    if width is None:
        width = pyxel.width - 1
    if height is None:
        height = pyxel.height - 1
    a, b, c, d = (x, y), (x + width, y), (x + width, y + height), (x, y + height)

    # noinspection PyProtectedMember
    if col is not None:
        kwargs["color"] = col
    opts = {k: kwargs.pop(k) for k in Body._init_kwargs if k in kwargs}
    body = Body(body_type=Body.STATIC, **opts)
    body.create_segment(a, b, **kwargs)
    body.create_segment(b, c, **kwargs)
    body.create_segment(c, d, **kwargs)
    body.create_segment(d, a, **kwargs)
    return body


class PhysSpace(Space):
    _init_kwargs = {*Space._init_kwargs, "background_color", "sub_steps", "camera"}
    background_color: int = 0
    sub_steps: int = 1
    camera: "Camera"

    def update(self, dt: float = 1 / getattr(pyxel, "DEFAULT_FPS", 30)):
        """
        Default update step for space.
        """
        self.step(dt, self.sub_steps, skip_events=("after-step",))

    def draw(self, clear: Union[bool, Color] = False):
        """
        Draw space on screen.
        """
        if clear is True:
            pyxel.cls(self.background_color)
        elif not isinstance(clear, bool):
            pyxel.cls(clear)
        self.debug_draw(self.draw_options)
        self._execute_step_handlers("after-step")

    def run(self):
        """
        Run pyxel engine alongside with physics.
        """
        pyxel.run(self.update, lambda: self.draw(clear=True))


# noinspection PyTypeHints
def space(
    bg: ColorT = pyxel.COLOR_BLACK,
    col: ColorT = pyxel.COLOR_WHITE,
    camera=pyxel,
    draw_options=None,
    wireframe: bool = False,
    friction: float = 0.0,
    elasticity: float = 0.0,
    sub_steps: int = 1,
    **kwargs
) -> PhysSpace:
    """
    Create a space object.

    Args:
        bg:
            Background color. If set to None, prevents clearing screen.
        col:
            Default foreground color.
        camera:
            A module of functions with all drawing functions of the Pyxel API.
            This can be used to implement cameras or to implement transformations
            before committing pixels to the screen.
        draw_options:
            An instance of :cls:`easymunk.pyxel.DebugDraw()`. Takes precedence
            over the camera and wireframe options.
        wireframe:
            Draw shapes in wireframe mode.
        elasticity:
            Default elasticity of shapes in space.
        friction:
            Default friction of shapes in space.
        sub_steps:
            The number of physics sub-steps to perform at each iteration.

    Keyword Args:
        It accepts arguments of :cls:`easymunk.Space`.
    """
    global DEFAULT_SPACE, DEFAULT_FRICTION, DEFAULT_ELASTICITY, DEFAULT_COLOR

    if draw_options is None:
        draw_options = DrawOptions(camera, wireframe=wireframe, keep_shape_colors=True)
    else:
        draw_options = draw_options

    kwargs["background_color"] = bg
    kwargs["sub_steps"] = sub_steps
    kwargs["camera"] = camera
    DEFAULT_FRICTION = friction
    DEFAULT_ELASTICITY = elasticity
    DEFAULT_COLOR = col
    DEFAULT_SPACE = PhysSpace(draw_options=draw_options, **kwargs)
    return DEFAULT_SPACE


def moment_multiplier(value: float = None) -> float:
    """
    Default multiplier used to calculate the moment of standard shapes.

    Call with argument to set value, and return value if called with no
    arguments.
    """
    global MOMENT_MULTIPLIER

    if value is None:
        return MOMENT_MULTIPLIER
    else:
        MOMENT_MULTIPLIER = float(value)
        return MOMENT_MULTIPLIER


def reset_space():
    """
    Reset the default space.
    """
    global DEFAULT_SPACE

    DEFAULT_SPACE = None
