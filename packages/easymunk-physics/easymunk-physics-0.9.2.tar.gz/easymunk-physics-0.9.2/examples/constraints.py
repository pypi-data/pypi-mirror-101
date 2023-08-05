"""
Pymunk constraints demo. Showcase of all the constraints included in easymunk.

Adapted from the Chipmunk Joints demo:
https://github.com/slembcke/Chipmunk2D/blob/master/demo/Joints.c
"""

import inspect
import math

import pygame

import easymunk
import easymunk.pygame
from easymunk import Vec2d

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


help_txt = font.render(
    "Pymunk constraints demo. Use mouse to drag/drop. Hover to see descr.",
    True,
    pygame.Color("darkgray"),
)

space = easymunk.Space()
space.gravity = (0.0, 900.0)
draw_options = easymunk.pygame.DrawOptions(screen)

# containers
box_size = 200
w = screen.get_width()
h = screen.get_height()
for i in range(6):
    sw = easymunk.Segment((0, i * box_size), (w, i * box_size), 1, space.static_body)
    sw.friction = 1
    sw.elasticity = 1
    sh = easymunk.Segment(
        (i * box_size, 0), (i * box_size, h - box_size), 1, space.static_body
    )
    sh.friction = 1
    sh.elasticity = 1
    space.add(sw, sh)


def add_ball(space, pos, box_offset):
    body = easymunk.Body()
    body.position = Vec2d(*pos) + box_offset
    shape = easymunk.Circle(20, body=body)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


def add_bar(space, pos, box_offset):
    body = easymunk.Body()
    body.position = Vec2d(*pos) + box_offset
    shape = easymunk.Segment((0, 40), (0, -40), 6, body)
    shape.mass = 2
    shape.friction = 0.7
    space.add(body, shape)
    return body


def add_lever(space, pos, box_offset):
    body = easymunk.Body()
    body.position = pos + Vec2d(*box_offset) + (0, -20)
    shape = easymunk.Segment((0, 20), (0, -20), 5, body)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


txts = {}

box_offset = 0, 0
b1 = add_ball(space, (50, 60), box_offset)
b2 = add_ball(space, (150, 60), box_offset)
c: easymunk.Constraint = easymunk.DistanceJoint(
    b1, b2, anchor_a=(20, 0), anchor_b=(-20, 0)
)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size, 0
b1 = add_ball(space, (50, 60), box_offset)
b2 = add_ball(space, (150, 60), box_offset)
c = easymunk.LimitDistanceJoint(b1, b2, 40, 80, (20, 0), (-20, 0))
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 2, 0
b1 = add_ball(space, (50, 60), box_offset)
b2 = add_ball(space, (150, 60), box_offset)
c = easymunk.PositionJoint(b1, b2, Vec2d(*box_offset) + (100, 60))
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 3, 0
b1 = add_ball(space, (50, 60), box_offset)
b2 = add_ball(space, (150, 60), box_offset)
c = easymunk.SegmentJoint(b1, b2, (50, 50), (50, -50), (-50, 0))
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 4, 0
b1 = add_ball(space, (50, 60), box_offset)
b2 = add_ball(space, (150, 60), box_offset)
c = easymunk.DampedSpring(b1, b2, 5, 0.3, 20, (30, 0), (-30, 0))
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 5, 0
b1 = add_bar(space, (50, 80), box_offset)
b2 = add_bar(space, (150, 80), box_offset)
# Add some joints to hold the circles in place.
space.add(easymunk.PositionJoint(b1, space.static_body, (50, 80) + Vec2d(*box_offset)))
space.add(easymunk.PositionJoint(b2, space.static_body, (150, 80) + Vec2d(*box_offset)))
c = easymunk.DampedRotarySpring(b1, b2, 3000, 60, 0)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = 0, box_size
b1 = add_lever(space, (50, 100), box_offset)
b2 = add_lever(space, (150, 100), box_offset)
# Add some joints to hold the circles in place.
space.add(easymunk.PositionJoint(b1, space.static_body, (50, 100) + Vec2d(*box_offset)))
space.add(
    easymunk.PositionJoint(b2, space.static_body, (150, 100) + Vec2d(*box_offset))
)
# Hold their rotation within 90 degrees of each other.
c = easymunk.LimitAngleJoint(b1, b2, math.pi / 2, math.pi / 2)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size, box_size
b1 = add_lever(space, (50, 100), box_offset)
b2 = add_lever(space, (150, 100), box_offset)
# Add some pin joints to hold the circles in place.
space.add(easymunk.PositionJoint(b1, space.static_body, (50, 100) + Vec2d(*box_offset)))
space.add(
    easymunk.PositionJoint(b2, space.static_body, (150, 100) + Vec2d(*box_offset))
)
# Ratchet every 90 degrees
c = easymunk.RatchetJoint(b1, b2, math.pi / 2, 0)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 2, box_size
b1 = add_bar(space, (50, 100), box_offset)
b2 = add_bar(space, (150, 100), box_offset)
# Add some pin joints to hold the circles in place.
space.add(easymunk.PositionJoint(b1, space.static_body, (50, 100) + Vec2d(*box_offset)))
space.add(
    easymunk.PositionJoint(b2, space.static_body, (150, 100) + Vec2d(*box_offset))
)
# Force one to sping 2x as fast as the other
c = easymunk.AngularRatioJoint(b1, b2, 2, 0)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

box_offset = box_size * 3, box_size
b1 = add_bar(space, (50, 100), box_offset)
b2 = add_bar(space, (150, 100), box_offset)
# Add some pin joints to hold the circles in place.
space.add(easymunk.PositionJoint(b1, space.static_body, (50, 100) + Vec2d(*box_offset)))
space.add(
    easymunk.PositionJoint(b2, space.static_body, (150, 100) + Vec2d(*box_offset))
)
# Make them spin at 1/2 revolution per second in relation to each other.
c = easymunk.AngularVelocityJoint(b1, b2, math.pi)
txts[box_offset] = inspect.getdoc(c)
space.add(c)

# TODO add one or two advanced constraints examples, such as a car or rope

mouse_joint = None
mouse_body = easymunk.Body(body_type=easymunk.Body.KINEMATIC)

# Build rendered help texts
box_texts = {}
for k in txts:
    l = 0
    box_texts[k] = []
    # Only take the first 5 lines.
    for line in txts[k].splitlines()[:5]:
        txt = font.render(line, True, pygame.Color("black"))
        box_texts[k].append(txt)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, easymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == easymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                mouse_joint = easymunk.PositionJoint(
                    mouse_body, shape.body, (0, 0), shape.body.world_to_local(nearest)
                )
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1 - 0.15) ** 60
                space.add(mouse_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

    screen.fill(pygame.Color("white"))

    screen.blit(help_txt, (5, screen.get_height() - 20))

    mouse_pos = pygame.mouse.get_pos()

    # Display help message
    x = mouse_pos[0] // box_size * box_size
    y = mouse_pos[1] // box_size * box_size

    if (x, y) in box_texts:
        txts = box_texts[(x, y)]
        i = 0
        for txt in txts:
            pos = (5, box_size * 2 + 10 + i * 20)
            screen.blit(txt, pos)
            i += 1

    mouse_body.position = mouse_pos

    space.step(1.0 / 60)

    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.set_caption(f"fps: {clock.get_fps()}")
