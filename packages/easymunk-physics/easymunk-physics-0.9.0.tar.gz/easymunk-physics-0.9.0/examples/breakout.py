"""Very simple breakout clone. A circle shape serves as the paddle, then 
breakable bricks constructed of Poly-shapes. 

The code showcases several pymunk concepts such as elasitcity, impulses, 
constant object speed, joints, collision handlers and post step callbacks.
"""

import random
import sys

import pygame

import easymunk
import easymunk.pygame
from easymunk import Vec2d

width, height = 600, 600


collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}


def spawn_ball(space, position, direction):
    ball_body = easymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = easymunk.Circle(5, body=ball_body)
    ball_shape.color = pygame.Color("green")
    ball_shape.elasticity = 1.0
    ball_shape.collision_type = collision_types["ball"]

    ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity

    space.add(ball_body, ball_shape)


def setup_level(space, player_body):

    # Remove balls and bricks
    for s in list(space.shapes):
        if s.body.body_type == easymunk.Body.DYNAMIC and s.body not in [player_body]:
            space.remove(s.body, s)

    # Spawn a ball for the player to have something to play with
    spawn_ball(
        space, player_body.position + (0, 40), random.choice([(1, 10), (-1, 10)])
    )

    # Spawn bricks
    for x in range(0, 21):
        x = x * 20 + 100
        for y in range(0, 5):
            y = y * 10 + 400
            brick_body = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
            brick_body.position = x, y
            brick_shape = easymunk.Poly.new_box((20, 10), body=brick_body)
            brick_shape.elasticity = 1.0
            brick_shape.color = pygame.Color("blue")
            brick_shape.group = 1
            brick_shape.collision_type = collision_types["brick"]
            space.add(brick_body, brick_shape)

    # Make bricks be removed when hit by ball
    def remove_brick(arbiter):
        brick_shape = arbiter.shapes[0]
        space.remove(brick_shape, brick_shape.body)

    h = space.collision_handler(collision_types["brick"], collision_types["ball"])
    h.separate = remove_brick


def main():
    # PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)
    # Physics stuff
    space = easymunk.Space()
    draw_options = easymunk.pygame.DrawOptions(screen, flip_y=True)

    # Game area
    # walls - the left-top-right walls
    static_lines = [
        easymunk.Segment((50, 50), (50, 550), 2, space.static_body),
        easymunk.Segment((50, 550), (550, 550), 2, space.static_body),
        easymunk.Segment((550, 550), (550, 50), 2, space.static_body),
    ]
    for line in static_lines:
        line.color = pygame.Color("lightgray")
        line.elasticity = 1.0

    space.add(*static_lines)

    # bottom - a sensor that removes anything touching it
    bottom = easymunk.Segment((50, 50), (550, 50), 2, space.static_body)
    bottom.sensor = True
    bottom.collision_type = collision_types["bottom"]
    bottom.color = pygame.Color("red")

    def remove_first(arbiter):
        ball_shape = arbiter.shapes[0]
        space.remove(ball_shape, ball_shape.body)
        return True

    h = space.collision_handler(collision_types["ball"], collision_types["bottom"])
    h.begin = remove_first
    space.add(bottom)

    # Player ship
    player_body = easymunk.Body(500, float("inf"))
    player_body.position = 300, 100

    player_shape = easymunk.Segment((-50, 0), (50, 0), 8, player_body)
    player_shape.color = pygame.Color("red")
    player_shape.elasticity = 1.0
    player_shape.collision_type = collision_types["player"]

    def pre_solve(arbiter):
        # We want to update the collision normal to make the bounce direction
        # dependent of where on the paddle the ball hits. Note that this
        # calculation isn't perfect, but just a quick example.
        pset = arbiter.contact_point_set
        if len(pset.points) > 0:
            player_shape = arbiter.shapes[0]
            width = (player_shape.b - player_shape.a).x
            delta = (player_shape.body.position - pset.points[0].point_a).x
            normal = Vec2d(0, 1).rotated(delta / width / 2)
            pset.copy(normal=normal, points=[pset.points[0].copy(distance=0)])
        arbiter.contact_point_set = pset
        return True

    h = space.collision_handler(collision_types["player"], collision_types["ball"])
    h.pre_solve = pre_solve

    # restrict movement of player to a straigt line
    move_joint = easymunk.SegmentJoint(
        space.static_body, player_body, (100, 100), (500, 100), (0, 0)
    )
    space.add(player_body, player_shape, move_joint)
    global state
    # Start game
    setup_level(space, player_body)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and (
                event.key in [pygame.K_ESCAPE, pygame.K_q]
            ):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "breakout.png")

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player_body.velocity = (-600, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                player_body.velocity = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player_body.velocity = (600, 0)
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                player_body.velocity = 0, 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                setup_level(space, player_body)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spawn_ball(
                    space,
                    player_body.position + (0, 40),
                    random.choice([(1, 10), (-1, 10)]),
                )

        # Clear screen
        screen.fill(pygame.Color("black"))

        # Draw stuff
        space.debug_draw(draw_options)

        state = []
        for x in space.shapes:
            s = "%s %s %s" % (x, x.body.position, x.body.velocity)
            state.append(s)

        # Update physics
        fps = 60
        dt = 1.0 / fps
        space.step(dt)

        # Info and flip screen
        screen.blit(
            font.render("fps: " + str(clock.get_fps()), 1, pygame.Color("white")),
            (0, 0),
        )
        screen.blit(
            font.render(
                "Move with left/right arrows, space to spawn a ball",
                1,
                pygame.Color("darkgrey"),
            ),
            (5, height - 35),
        )
        screen.blit(
            font.render(
                "Press R to reset, ESC or Q to quit", 1, pygame.Color("darkgrey")
            ),
            (5, height - 20),
        )

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    sys.exit(main())
