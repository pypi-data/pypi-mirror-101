"""Showcase of flying arrows that can stick to objects in a somewhat 
realistic looking way.
"""
import sys
from typing import List

import pygame

import easymunk as mk
from easymunk import Vec2d, Space, pygame as mk_pygame


def create_arrow(space: Space):
    return space.create_poly(
        [(-30, 0), (0, 3), (10, 0), (0, -3)],
        body_type="kinematic",
        friction=0.5,
        collision_type=1,
        density=0.1,
    )


def stick_arrow_to_target(space, arrow_body, target_body, position):
    pivot_joint = mk.PositionJoint(arrow_body, target_body, position)
    phase = target_body.angle - arrow_body.angle
    gear_joint = mk.AngularRatioJoint(arrow_body, target_body, 1, phase)
    space.add(pivot_joint)
    space.add(gear_joint)
    try:
        flying_arrows.remove(arrow_body)
    except:
        pass


def post_solve_arrow_hit(arbiter):
    if arbiter.total_impulse.length > 300:
        a, b = arbiter.shapes
        position = arbiter.contact_point_set.points[0].point_a
        b.collision_type = 0
        b.group = 1
        other_body = a.body
        arrow_body = b.body
        arbiter.space.add_post_step_callback(
            stick_arrow_to_target,
            arrow_body,
            other_body,
            position,
        )


width, height = 690, 600
flying_arrows: List[mk.Body] = []


def main():
    # PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)

    # Physics stuff
    space = mk.Space(gravity=(0, 1000))
    draw_options = mk.pygame.DrawOptions(screen)

    # walls - the left-top-right walls
    static: List[mk.Shape] = [
        mk.Segment((50, 550), (50, 50), 5, space.static_body),
        mk.Segment((50, 50), (650, 50), 5, space.static_body),
        mk.Segment((650, 50), (650, 550), 5, space.static_body),
        mk.Segment((50, 550), (650, 550), 5, space.static_body),
    ]

    b2 = mk.Body(body_type=mk.Body.KINEMATIC)
    static.append(mk.Circle(30, body=b2))
    b2.position = 300, 200

    for s in static:
        s.friction = 1.0
        s.group = 1
    space.add(b2, *static)

    # "Cannon" that can fire arrows
    cannon_body = mk.Body(body_type=mk.Body.KINEMATIC)
    cannon_shape = mk.Circle(25, body=cannon_body)
    cannon_shape.sensor = True
    cannon_shape.color = (255, 50, 50, 255)
    cannon_body.position = 100, 500
    space.add(cannon_body, cannon_shape)

    arrow_body = create_arrow(space)

    handler = space.collision_handler(0, 1)
    handler.post_solve = post_solve_arrow_hit

    while running:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and (event.key in [pygame.K_ESCAPE, pygame.K_q])
            ):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "arrows.png")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                end_time = pygame.time.get_ticks()

                diff = end_time - start_time
                power = max(min(diff, 1000), 10) * 13.5
                impulse = power * Vec2d(1, 0)
                impulse = impulse.rotated(arrow_body.angle)
                arrow_body.body_type = "dynamic"
                arrow_body.apply_impulse_at_world_point(impulse, arrow_body.position)

                flying_arrows.append(arrow_body)
                arrow_body = create_arrow(space)

        keys = pygame.key.get_pressed()

        speed = 2.5
        if keys[pygame.K_UP]:
            cannon_body.position += Vec2d(0, 1) * speed
        if keys[pygame.K_DOWN]:
            cannon_body.position += Vec2d(0, -1) * speed
        if keys[pygame.K_LEFT]:
            cannon_body.position += Vec2d(-1, 0) * speed
        if keys[pygame.K_RIGHT]:
            cannon_body.position += Vec2d(1, 0) * speed

        mouse_position = draw_options.mouse_pos()
        cannon_body.angle = (mouse_position - cannon_body.position).angle

        # move the unfired arrow together with the cannon
        arrow_body.position = cannon_body.position + Vec2d(
            cannon_shape.radius + 40, 0
        ).rotated(cannon_body.angle)
        arrow_body.angle = cannon_body.angle

        for flying_arrow in flying_arrows:
            drag_constant = 0.0002

            pointing_direction = Vec2d(1, 0).rotated(flying_arrow.angle)
            flight_direction = Vec2d(*flying_arrow.velocity)
            flight_direction, flight_speed = flight_direction.normalized_and_length()

            dot = flight_direction.dot(pointing_direction)
            # (1-abs(dot)) can be replaced with (1-dot) to make arrows turn
            # around even when fired straight up. Might not be as accurate, but
            # maybe look better.
            drag_force_magnitude = (
                (1 - abs(dot)) * flight_speed ** 2 * drag_constant * flying_arrow.mass
            )
            arrow_tail_position = flying_arrow.position + Vec2d(-50, 0).rotated(
                flying_arrow.angle
            )
            flying_arrow.apply_impulse_at_world_point(
                drag_force_magnitude * -flight_direction, arrow_tail_position
            )

            flying_arrow.angular_velocity *= 0.5

        # Clear screen
        screen.fill(pygame.Color("black"))

        # Draw stuff
        space.debug_draw(draw_options)
        # draw(screen, space)

        # Power meter
        if pygame.mouse.get_pressed()[0]:
            current_time = pygame.time.get_ticks()
            diff = current_time - start_time
            power = max(min(diff, 1000), 10)
            h = power // 2
            pygame.draw.line(screen, pygame.Color("red"), (30, 550), (30, 550 - h), 10)

        # Info and flip screen
        screen.blit(
            font.render("fps: " + str(clock.get_fps()), True, pygame.Color("white")),
            (0, 0),
        )
        screen.blit(
            font.render(
                "Aim with mouse, hold LMB to powerup, release to fire",
                True,
                pygame.Color("darkgrey"),
            ),
            (5, height - 35),
        )
        screen.blit(
            font.render("Press ESC or Q to quit", True, pygame.Color("darkgrey")),
            (5, height - 20),
        )

        pygame.display.flip()

        # Update physics
        fps = 60
        dt = 1.0 / fps
        space.step(dt)

        clock.tick(fps)


if __name__ == "__main__":
    sys.exit(main())
