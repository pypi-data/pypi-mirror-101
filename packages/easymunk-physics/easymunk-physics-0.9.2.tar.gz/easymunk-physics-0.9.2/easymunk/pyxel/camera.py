from math import copysign
from typing import Union


from sidekick.properties import alias, delegate_to, property as property_

from ..linalg import Vec2d
from ..typing import VecLike
from .draw_options import draw, drawb
from .helpers import get_pyxel


# TODO: in the future we should merge camera with DrawOptions
class Camera:
    """
    A camera rendering module that renders with an offset.

    It emulates the Pyxel module API but executes any necessary coordinate
    transformation before rendering data to the screen.
    """

    flip_y: bool = alias("_flip_y")

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = Vec2d(*value)

    # Missing:
    # pyxel.image
    # pyxel.Image
    # pyxel.Tilemap

    # We declare some delegations to make static analysis happy
    mouse_x: int = delegate_to("_mod")
    mouse_y: int = property_(lambda self: self._y(self._mod.mouse_y))
    width: int = delegate_to("_mod")
    height: int = delegate_to("_mod")
    btn = delegate_to("_mod")
    btnp = delegate_to("_mod")
    btnr = delegate_to("_mod")

    # noinspection PyShadowingNames
    def __init__(self, offset=(0, 0), mod=None, flip_y: bool = False):
        self._mod = mod or get_pyxel()
        self.offset: Vec2d = offset
        self._y_sign = -1 if flip_y else 1
        self._flip_y = flip_y

    def __getattr__(self, attr):
        if attr.startswith("_"):
            # Cache module attributes
            try:
                fn = getattr(self._mod, attr[1:])
            except AttributeError:
                raise
            else:
                setattr(self, attr, fn)
                return fn
        return getattr(self._mod, attr)

    def _y(self, y, h=0):
        return self._mod.height - y - 1 - h if self._flip_y else y

    def follow(self, center: VecLike, tol: Union[float, VecLike] = 0.0) -> None:
        """
        Center camera in the given point.

        Args:
            center: Position to center camera.
            tol:
                a number or tuple of numbers with the tolerance for which the
                center can deviate from the target position.
        """
        width, height = self._mod.width, self._mod.height
        target = center - Vec2d(width / 2, height / 2)
        if not tol:
            self._offset = target
        else:
            try:
                xtol, ytol = tol  # type: ignore
            except TypeError:
                xtol = ytol = tol
            dx, dy = target - self._offset
            self._offset += Vec2d(
                copysign(max(abs(dx) - xtol, 0), dx),
                copysign(max(abs(dy) - ytol, 0), dy),
            )

    def pan_right(self, step: float) -> None:
        """
        Move camera right by step.
        """
        self._offset += (step, 0)

    def pan_left(self, step: float) -> None:
        """
        Move camera left by step.
        """
        self._offset -= (step, 0)

    def pan_up(self, step: float) -> None:
        """
        Move camera up by step.
        """
        self._offset += (0, self._y_sign * step)

    def pan_down(self, step: float) -> None:
        """
        Move camera down by step.
        """
        self._offset -= (0, self._y_sign * step)

    def pset(self, x: int, y: int, col: int) -> None:
        x0, y0 = self._offset
        self._pset(x - x0, self._y(y - y0), col)

    def pget(self, x: int, y: int) -> None:
        x0, y0 = self._offset
        self._pget(x - x0, self._y(y - y0))

    def circ(self, x: int, y: int, r: int, col: int) -> None:
        x0, y0 = self._offset
        self._circ(x - x0, self._y(y - y0), r, col)

    def circb(self, x: int, y: int, r: int, col: int) -> None:
        x0, y0 = self._offset
        self._circb(x - x0, self._y(y - y0), r, col)

    def line(self, x1: int, y1: int, x2: int, y2: int, col: int) -> None:
        f = self._y
        x0, y0 = self._offset
        self._line(x1 - x0, f(y1 - y0), x2 - x0, f(y2 - y0), col)

    def tri(
        self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, col: int
    ) -> None:
        x0, y0 = self._offset
        yy = self._y
        self._tri(
            x1 - x0,
            yy(y1 - y0),
            x2 - x0,
            yy(y2 - y0),
            x3 - x0,
            yy(y3 - y0),
            col,
        )

    def trib(
        self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, col: int
    ) -> None:
        x0, y0 = self._offset
        yy = self._y
        self._trib(
            x1 - x0,
            yy(y1 - y0),
            x2 - x0,
            yy(y2 - y0),
            x3 - x0,
            yy(y3 - y0),
            col,
        )

    def rect(self, x: int, y: int, w: int, h: int, col: int) -> None:
        x0, y0 = self._offset
        self._rect(x - x0, self._y(y - y0, h), w, h, col)

    def rectb(self, x: int, y: int, w: int, h: int, col: int) -> None:
        x0, y0 = self._offset
        self._rectb(x - x0, self._y(y - y0, h), w, h, col)

    def text(self, x: int, y: int, s: str, col: int) -> None:
        x0, y0 = self._offset
        self._text(x - x0, self._y(y - y0, self._FONT_HEIGHT), s, col)

    def blt(
        self, x: int, y: int, img: int, u: int, v: int, w: int, h: int, colkey: int = -1
    ) -> None:
        x0, y0 = self._offset
        return self._blt(x - x0, self._y(y - y0, h), img, u, v, w, h, colkey)

    def bltm(
        self, x: int, y: int, tm: int, u: int, v: int, w: int, h: int, colkey: int = -1
    ) -> None:
        x0, y0 = self._offset
        return self._bltm(x - x0, self._y(y - y0, 8 * h), tm, u, v, w, h, colkey)

    def draw(self, obj, col=None):
        f"""{draw}"""
        return draw(obj, mod=self, col=col)

    def drawb(self, obj, col=None):
        f"""{drawb}"""
        return drawb(obj, mod=self, col=col)
