"""Very simple example that does not depend on any third party library such 
as pygame or pyglet like the other examples. 
"""

import math
import random
import sys

import easymunk
import easymunk.util
from easymunk import Vec2d


def main():
    print(f"basic example of pymunk {easymunk.__version__}")
    space = easymunk.Space()
    space.gravity = (0.0, -900.0)

    ## Balls
    balls = []

    ticks_to_next_ball = 10
    for x in range(5000):
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 10000
            mass = 10
            radius = 25
            inertia = easymunk.moment_for_circle(mass, radius, 0, (0, 0))
            body = easymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 400
            shape = easymunk.Circle(radius, Vec2d(0, 0), body)
            space.add(body, shape)
            balls.append(shape)

        balls_to_remove = []

        for ball in balls:
            if ball.body.position.y < 0:
                balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        if len(balls) >= 1:
            v = balls[0].body.position
            print("(in on_draw): point = %.2f, %.2f" % (v.x, v.y))

        # Update physics
        for x in range(1):
            space.step(1 / 50.0)
    print("done!")


if __name__ == "__main__":
    sys.exit(main())
