from typing import Callable

from .core import Body
from .util import typed
from .linalg import Vec2d
from .typing import VecLike

VelocityFunc = Callable[["Body", Vec2d, float, float], None]


def velocity_func(gravity: VecLike = None, damping: float = None) -> VelocityFunc:
    """
    Create a velocity function that possibly fix the gravity and damping.
    """

    fn = Body.update_velocity
    if gravity is None and damping is None:
        velocity_function = fn
    elif damping is None:

        def velocity_function(body, _, damping, dt):
            return fn(body, gravity, damping, dt)

    elif gravity is None:

        def velocity_function(body, gravity, _, dt):
            return fn(body, gravity, damping, dt)

    else:

        def velocity_function(body, _, __, dt):
            return fn(body, gravity, damping, dt)

    return velocity_function


def max_speed(value: float) -> VelocityFunc:
    """
    Create a velocity function that limits velocity after updating.
    """

    @typed(VelocityFunc)
    def velocity_function(body, gravity, damping, dt):
        Body.update_velocity(body, gravity, damping, dt)

        vel = body.velocity
        if (speed := vel.length) > value:
            body.velocity = speed / value * vel

    return velocity_function


@typed(VelocityFunc)
def velocity_function_inertia(body, gravity, damping, dt):
    """
    Do nothing when updating velocity.
    """
