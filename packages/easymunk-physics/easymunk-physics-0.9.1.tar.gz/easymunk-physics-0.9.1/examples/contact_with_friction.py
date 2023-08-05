"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Displays collsion strength and rotating balls thanks to 
friction. Not interactive.
"""

import random
import sys

import pygame

import easymunk
import easymunk.pygame


def draw_collision(arbiter):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = draw_options.to_pygame(c.point_a, screen)
        pygame.draw.circle(screen, pygame.Color("black"), p, r, 1)


def main():
    global screen

    clock = pygame.time.Clock()
    running = True

    # Physics stuff
    space = easymunk.Space()
    space.gravity = (0.0, -900.0)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = (
        draw_options.flags ^ easymunk.pygame.DrawOptions.DRAW_COLLISION_POINTS
    )
    # Balls
    balls = []

    # walls
    static_lines = [
        easymunk.Segment((11.0, 280.0), (407.0, 246.0), 0.0, space.static_body),
        easymunk.Segment((407.0, 246.0), (407.0, 343.0), 0.0, space.static_body),
    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(*static_lines)

    ticks_to_next_ball = 10

    ch = space.collision_handler(0, 0)
    ch.post_solve = draw_collision

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "contact_with_friction.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 100
            mass = 0.1
            radius = 25
            inertia = easymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = easymunk.Body(mass, inertia)
            x = random.randint(115, 350)
            body.position = x, 400
            shape = easymunk.Circle(radius, (0, 0), body)
            shape.friction = 0.5
            space.add(body, shape)
            balls.append(shape)

        # Clear screen
        screen.fill(pygame.Color("white"))

        # Draw stuff
        space.debug_draw(draw_options)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 200:
                balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        # Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        # Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


pygame.init()
screen = pygame.display.set_mode((600, 600))
draw_options = easymunk.pygame.DrawOptions(screen, flip_y=True)

if __name__ == "__main__":
    sys.exit(main())
