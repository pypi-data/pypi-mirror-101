"""This submodule contains helper functions to help with quick prototyping 
using pymunk together with pyglet.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not very optimized (they use batched 
drawing, but there is probably room for optimizations still). 
"""
import io
from typing import Sequence

import matplotlib.pyplot as plt  # type: ignore
from matplotlib.axes import Axes

from ..abc import CpCFFIBase
from ..drawing import Color, DrawOptions as DrawOptionsBase
from ..linalg import Vec2d
from ..typing import VecLike, BBLike


class DrawOptions(DrawOptionsBase):
    _COLOR = DrawOptionsBase._COLOR

    def __init__(self, ax: Axes = None, bb: BBLike = None, dot_scale=0.1) -> None:
        """DrawOptions for space.debug_draw() to draw a space on a ax object.

        Typical usage::

        >>> space = mk.Space()
        >>> space.debug_draw("matplotlib")

        You can control the color of a Shape by setting shape.color to the color
        you want it drawn in.

        >>> shape = space.static_body.create_circle(10)
        >>> shape.color = (1, 0, 0, 1) # will draw shape in red

        See matplotlib_util.demo.py for a full example

        :Param:
            ax: matplotlib.Axes
                A matplotlib Axes object.

        """
        super(DrawOptions, self).__init__()
        self._ax = ax
        self.bb = bb
        self.dot_scale = dot_scale

    @property
    def ax(self) -> Axes:
        return self._ax or plt.gca()

    def draw_circle(
        self,
        pos: VecLike,
        radius: float,
        angle: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        p = plt.Circle(  # type: ignore
            pos,
            radius,
            facecolor=fill_color.as_float(),
            edgecolor=outline_color.as_float(),
        )
        self.ax.add_patch(p)

        circle_edge = pos + Vec2d(radius, 0).rotated_radians(angle)
        line = plt.Line2D(  # type: ignore
            [pos[0], circle_edge[0]],
            [pos[1], circle_edge[1]],
            linewidth=1,
            color=outline_color.as_float(),
        )
        line.set_solid_capstyle("round")  # type: ignore
        self.ax.add_line(line)

    def draw_segment(self, a: VecLike, b: VecLike, color: Color = _COLOR) -> None:
        line = plt.Line2D(a, b, linewidth=1, color=color.as_float())  # type: ignore
        line.set_solid_capstyle("round")  # type: ignore
        self.ax.add_line(line)

    def draw_fat_segment(
        self,
        a: VecLike,
        b: VecLike,
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        radius = max(1.0, 2.0 * radius)
        line = plt.Line2D(  # type: ignore
            [a[0], b[0]], [a[1], b[1]], linewidth=radius, color=fill_color.as_float()
        )
        line.set_solid_capstyle("round")  # type: ignore
        self.ax.add_line(line)

    def draw_polygon(
        self,
        verts: Sequence[VecLike],
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        radius = max(1.0, 2.0 * radius)
        p = plt.Polygon(  # type: ignore
            verts,
            closed=True,
            linewidth=radius,
            joinstyle="round",
            facecolor=fill_color.as_float(),
            edgecolor=outline_color.as_float(),
        )
        self.ax.add_patch(p)

    def draw_dot(self, size: float, pos: VecLike, color: Color) -> None:
        color = color.as_float()
        radius = self.dot_scale * size
        p = plt.Circle(pos, radius, facecolor=color, edgecolor="None")  # type: ignore
        self.ax.add_patch(p)

    def finalize_frame(self):
        ax = self.ax
        if self.bb:
            x1, y1, x2, y2 = self.bb
            ax.axis([x1, x2, y1, y2])
        else:
            ax.autoscale()
        ax.set_aspect("equal")


def draw_object(obj, bb: "BBLike" = None, ax=None):
    """
    Draw easymunk object using matplotlib.
    """
    options = DrawOptions(ax or plt.gca(), bb=bb)
    options.draw_object(obj)
    return ax


def draw_svg(obj, bb: "BBLike" = None, ax=None, file=None) -> str:
    """
    Draw easymunk object using matplotlib and return an SVG string.
    """
    ax = draw_object(obj, bb, ax)
    fig = ax.get_figure()
    data = file if file is not None else io.StringIO()
    fig.savefig(data, format="svg")
    if file is not None:
        return data.getvalue()


class MatplotlibRenderer:
    """
    IPython renderer interface.
    """

    empty_renderer = False

    def save_fig(self, fmt, is_bytes=False):
        ax = draw_object(self)
        fig = ax.get_figure()
        fd = io.BytesIO() if is_bytes else io.StringIO()
        fig.savefig(fd, format=fmt)
        return fd if is_bytes else fd.getvalue()

    def html(self):
        return self.save_fig("svg", False)

    def javascript(self):
        return self.save_fig("js", False)

    def svg(self):
        return self.save_fig("svg", False)

    def png(self):
        return self.save_fig("png", True)

    def jpeg(self):
        return self.save_fig("jpeg", True)


if CpCFFIBase._ipython_renderer.empty_renderer:
    CpCFFIBase._ipython_renderer = MatplotlibRenderer()
