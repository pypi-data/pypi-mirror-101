"""A L shape attached with a joint and constrained to not tip over.

This example is also used in the Get Started Tutorial. 
"""

__docformat__ = "reStructuredText"

import random
import sys

import pygame

import easymunk
import easymunk.pygame

random.seed(1)


def add_ball(space):
    """Add a ball to the given space at a random position"""
    mass = 1
    radius = 14
    inertia = easymunk.moment_for_circle(mass, radius, 0, (0, 0))
    body = easymunk.Body(mass, inertia)
    x = random.randint(120, 380)
    body.position = x, 50
    shape = easymunk.Circle(radius, (0, 0), body)
    shape.friction = 1
    space.add(body, shape)
    return shape


def add_L(space):
    """Add a inverted L shape with two joints"""
    rotation_center_body = easymunk.Body(body_type=easymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = easymunk.Body(body_type=easymunk.Body.STATIC)
    rotation_limit_body.position = (200, 300)

    body = easymunk.Body(10, 10000)
    body.position = (300, 300)
    l1 = easymunk.Segment((-145, 0), (255.0, 0.0), 1, body)
    l2 = easymunk.Segment((-145, 0), (-145.0, -25.0), 1, body)
    l1.friction = 1
    l2.friction = 1
    rotation_center_joint = easymunk.DistanceJoint(
        body, rotation_center_body, anchor_a=(0, 0), anchor_b=(0, 0)
    )
    joint_limit = 25
    rotation_limit_joint = easymunk.LimitDistanceJoint(
        body, rotation_limit_body, 0, joint_limit, (-100, 0), (0, 0)
    )

    space.add(body, rotation_center_joint, rotation_limit_joint)
    return l1, l2


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = easymunk.Space()
    space.gravity = (0.0, 900.0)

    lines = add_L(space)
    balls = []
    draw_options = easymunk.pygame.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "slide_and_pinjoint.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y > 450:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    main()
