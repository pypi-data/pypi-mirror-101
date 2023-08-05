"""Showcase what the output of easymunk.pygame_util draw methods will look like.

See pyglet_util_demo.py for a comparison to pyglet.
"""

__docformat__ = "reStructuredText"

import sys

import pygame
import shapes_for_draw_demos

import easymunk
import easymunk.pygame
from easymunk.vec2d import Vec2d


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    space = easymunk.Space()
    captions = shapes_for_draw_demos.fill_space(space)

    # Draw it
    screen.fill(pygame.Color("white"))

    options = easymunk.pygame.DrawOptions(screen, flip_y=True)
    space.debug_draw(options)
    # easymunk.pygame_util.draw(screen, space)

    # Info
    color = pygame.Color("black")
    screen.blit(
        font.render("Demo example of pygame_util.DrawOptions()", True, color),
        (205, 680),
    )
    for caption in captions:
        x, y = caption[0]
        y = 700 - y
        screen.blit(font.render(caption[1], True, color), (x, y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and (event.key in [pygame.K_ESCAPE, pygame.K_q])
            ):
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "pygame_util_demo.png")

        clock.tick(10)


if __name__ == "__main__":
    sys.exit(main())
