import math
from typing import TYPE_CHECKING, Any, Optional, Sequence, Type
from functools import lru_cache
import pyglet  # type: ignore

from ..drawing import DrawOptions as DrawOptionsBase, Color
from ..linalg import Vec2d

if TYPE_CHECKING:
    from types import TracebackType


class DrawOptions(DrawOptionsBase):
    _COLOR = DrawOptionsBase._COLOR

    def __init__(self, **kwargs: Any) -> None:
        """Draw a Space object.

        Args:
            kwargs:
                You can optionally pass in a pyglet.graphics.Batch. If a batch
                is given all drawing will use this batch to draw on. If no
                batch is given a a new batch will be used for the drawing.
                Remember that if you pass in your own batch you need to call
                draw on it yourself.
        """
        self.new_batch = False

        if "batch" not in kwargs:
            self.new_batch = True
        else:
            self.batch = kwargs["batch"]

        super(DrawOptions, self).__init__()

    def __enter__(self) -> None:
        if self.new_batch:
            self.batch = pyglet.graphics.Batch()

    def __exit__(
        self,
        typ: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional["TracebackType"],
    ):
        if self.new_batch:
            self.batch.draw()

    def draw_circle(
        self,
        pos: Vec2d,
        radius: float,
        angle: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        circle_center = pos

        # http://slabode.exofire.net/circle_draw.shtml
        num_segments = int(4 * math.sqrt(radius))
        theta = 2 * math.pi / num_segments
        c = math.cos(theta)
        s = math.sin(theta)

        x = radius  # we start at angle 0
        y: float = 0

        ps = []

        for i in range(num_segments):
            ps += [Vec2d(circle_center.x + x, circle_center.y + y)]
            t = x
            x = c * x - s * y
            y = s * t + c * y

        mode = pyglet.gl.GL_TRIANGLE_STRIP
        ps2 = [ps[0]]
        for i in range(1, int(len(ps) + 1 / 2)):
            ps2.append(ps[i])
            ps2.append(ps[-i])
        ps = ps2
        vs = []
        for p in [ps[0]] + ps + [ps[-1]]:
            vs += [p.x, p.y]

        cc = circle_center + Vec2d(radius, 0).rotated(angle)
        cvs = [circle_center.x, circle_center.y, cc.x, cc.y]

        bg = pyglet.graphics.OrderedGroup(0)
        fg = pyglet.graphics.OrderedGroup(1)

        n = len(vs) // 2
        self.batch.add(len(vs) // 2, mode, bg, ("v2f", vs), ("c4B", fill_color * n))
        self.batch.add(
            2, pyglet.gl.GL_LINES, fg, ("v2f", cvs), ("c4B", outline_color * 2)
        )

    def draw_segment(self, a: Vec2d, b: Vec2d, color: Color = _COLOR) -> None:
        pv1 = a
        pv2 = b
        line = (int(pv1.x), int(pv1.y), int(pv2.x), int(pv2.y))

        self.batch.add(2, pyglet.gl.GL_LINES, None, ("v2i", line), ("c4B", color * 2))

    def draw_fat_segment(
        self,
        a: Vec2d,
        b: Vec2d,
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        pv1 = a
        pv2 = b
        d = pv2 - pv1
        atan = -math.atan2(d.x, d.y)
        radius = max(radius, 1)
        dx = radius * math.cos(atan)
        dy = radius * math.sin(atan)

        p1 = pv1 + Vec2d(dx, dy)
        p2 = pv1 - Vec2d(dx, dy)
        p3 = pv2 + Vec2d(dx, dy)
        p4 = pv2 - Vec2d(dx, dy)

        vs = [i for xy in [p1, p2, p3] + [p2, p3, p4] for i in xy]

        n = len(vs) // 2
        self.batch.add(
            n,
            pyglet.gl.GL_TRIANGLES,
            None,
            ("v2f", vs),
            ("c4B", fill_color * n),
        )

        self.draw_circle(a, radius, 0, fill_color, fill_color)
        self.draw_circle(b, radius, 0, fill_color, fill_color)

    def draw_polygon(
        self,
        verts: Sequence[Vec2d],
        radius: float = 0.0,
        outline_color: Color = _COLOR,
        fill_color: Color = _COLOR,
    ) -> None:
        mode = pyglet.gl.GL_TRIANGLE_STRIP

        n = len(verts)
        mid = len(verts) // 2
        if radius >= 3:
            # print("POLY", verts)
            pass
        vs = []
        for i in range(mid):
            vs += [verts[i].x, verts[i].y]
            vs += [verts[n - 1 - i].x, verts[n - 1 - i].y]

        if n % 2:
            vs += [verts[mid].x, verts[mid].y]

        vs = [vs[0], vs[1]] + vs + [vs[-2], vs[-1]]

        n = len(vs) // 2
        self.batch.add(n, mode, None, ("v2f", vs), ("c4B", fill_color * n))

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                self.draw_fat_segment(a, b, radius, outline_color, outline_color)

    def draw_dot(self, size: float, pos: Vec2d, color: Color) -> None:
        self.batch.add(
            1,
            pyglet.gl.GL_POINTS,
            _gr_point_size_cls()(size),
            ("v2f", pos),
            ("c4B", color * 1),
        )


@lru_cache()
def _gr_point_size_cls():
    # We wrap class creation since tests may fail if pyglet cannot find the
    # display
    class GrPointSize(pyglet.graphics.Group):  # type: ignore
        """
        This pyglet rendering group sets a specific point size.
        """

        def __init__(self, size: float = 1.0) -> None:
            super().__init__()
            self.size = size

        def set_state(self) -> None:
            pyglet.gl.glPointSize(self.size)

        def unset_state(self) -> None:
            pyglet.gl.glPointSize(1.0)

    return GrPointSize
