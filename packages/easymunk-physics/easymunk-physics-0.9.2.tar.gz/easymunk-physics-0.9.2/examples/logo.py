"""
A very simple script to create the Easymunk Logo from pixel-art.

It opens a screen with the logo. Press Alt+1 to save a screenshot to the
desktop.
"""
import pyxel
from easymunk import pyxel as phys

# It creates a simple triangle with a circle. L refers to the size of the
# triangle and x0 shifts the whole figure to the right.
L = 12
x0 = 2
circ_color = pyxel.COLOR_LIGHTBLUE
tri_color = pyxel.COLOR_ORANGE

# Init pyxel
pyxel.init(16, 16)

# We use easymunk's pyxel API to create space and objects. It lives on
# easymunk.pyxel and is usually aliased as phys. There you can use familiar
# pyxel-like functions to create objects in space (rather than painting them
# on screen).
space = phys.space(camera=phys.Camera(flip_y=True), wireframe=True)
phys.tri(x0, 1, x0 + L, 1, x0 + L, L + 1, tri_color, body_type="kinematic")
phys.circ(4 + x0, 9, 4, circ_color, angle=45, body_type="dynamic")

# Space instances created with phys.space have a run() method that triggers a
# minimalistic main loop. This is useful for very simple situations in which
# we just want to run the physics and paint the space objects's on the screen.
space.run()
