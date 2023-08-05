"""
Pymunk is a easy-to-use pythonic 2d physics library that can be used whenever
you need 2d rigid body physics from Python.

Homepage: http://www.easymunk.org

This is the main containing module of easymunk. It contains among other things
the very central Space, Body and Shape classes.
"""
# flake8: noqa
from sidekick.api import import_later
from typing import TYPE_CHECKING
from .core import (
    AngularRatioJoint,
    AngularVelocityJoint,
    Arbiter,
    Body,
    Circle,
    CircleBody,
    CollisionHandler,
    Constraint,
    DampedRotarySpring,
    DampedSpring,
    DistanceJoint,
    LimitAngleJoint,
    LimitDistanceJoint,
    Poly,
    PolyBody,
    PositionJoint,
    RatchetJoint,
    Segment,
    SegmentBody,
    SegmentJoint,
    Shape,
    Space,
)
from . import _version
from .geometry import (
    area_for_circle,
    area_for_poly,
    area_for_segment,
    convex_decomposition,
    is_closed,
    march_hard,
    march_soft,
    march_string,
    moment_for_box,
    moment_for_circle,
    moment_for_poly,
    moment_for_segment,
    simplify_curves,
    simplify_vertexes,
    to_convex_hull,
)
from .types import (
    BB,
    ContactPoint,
    ContactPointSet,
    PointQueryInfo,
    SegmentQueryInfo,
    ShapeFilter,
    ShapeQueryInfo,
)
from .drawing import DrawOptions
from .linalg import Vec2d, Transform, Mat22

__version__: str = _version.version
"""The release version of this installation.
Valid only if pymunk was installed from a source or binary
distribution (i.e. not in a checked-out copy from git).
"""

chipmunk_version: str = _version.chipmunk_version
"""The Chipmunk version used with this Pymunk version.

This property does not show a valid value in the compiled documentation, only
when you actually import easymunk and do easymunk.chipmunk_version

The string is in the following format:
<cpVersionString>R<github commit of chipmunk>
where cpVersionString is a version string set by Chipmunk and the git commit
hash corresponds to the git hash of the chipmunk source from
github.com/viblo/Chipmunk2D included with easymunk.
"""


# Fake import of utility modules. We want static checker to point to actual
# modules, but runtime should load them lazily
LAZY_MODULES = frozenset({"pyxel", "pygame", "pyglet", "matplotlib", "streamlit"})
if TYPE_CHECKING:
    from . import pyxel
    from . import pygame
    from . import pyglet
    from . import matplotlib
    from . import streamlit
    from .linalg import math


def __getattr__(name, valid=LAZY_MODULES):
    if name == "math":
        from .linalg import math

        return math

    if name in valid:
        return __import__(f"{__name__}.{name}")
    raise AttributeError(name)


del import_later, TYPE_CHECKING
