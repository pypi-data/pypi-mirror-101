import pyxel

import easymunk as mk
from easymunk import pyxel as phys, Arbiter, Vec2d

scenario = """
             ====    ====    ====                                             
                                                                              
         ====                     ====                                        
                                                                              
========                             ====            ===                     
                                                   ==========                 
             o                           x      ===================           
==============                       =========================================
******************************************************************************
******************************************************************************
"""
# scenario = (' === === \n'
#             ' ==  === \n'
#             ' =   === \n')

camera = phys.Camera(flip_y=True)
pyxel.init(256, 196)
camera.follow((128, 98))

pyxel.mouse(True)
space = phys.space(gravity=(0, -100), camera=camera, wireframe=True, sub_steps=4)
c1 = [phys.circ(x + 10, 128, 8) for x in range(0, 500, 40)]
space.shapes.filter(is_circle=True).apply(elasticity=0.5)
space.shapes.apply(friction=1.0)

player = phys.circ(4, 28, 4, color=pyxel.COLOR_RED, elasticity=0.0, collision_type=1)
player.can_jump = False

lines = mk.march_string(scenario, "=", scale=(8, 8), flip_y=True)
for ln in lines:
    b = phys.poly(ln, body_type="static", color=pyxel.COLOR_CYAN)

lines = mk.march_string(scenario, "*", scale=(8, 8), flip_y=True)
for ln in lines:
    print(ln)
    b = phys.poly(ln, body_type="static", color=pyxel.COLOR_CYAN)


bb = space.cache_bb()
phys.margin(bb.left, bb.bottom, bb.width, bb.height + 100, radius=5)
space.shapes.apply(friction=0, elasticity=1.0)
player.elasticity = 0.0


@space.post_solve_collision(1, ...)
def _(arb: Arbiter):
    n = arb.normal_from(player)
    player.can_jump = n.y < -0.5


@space.separate_collision(1, ...)
def _(arb: Arbiter):
    player.can_jump = False


@space.before_step()
def update():
    speed = 90
    jump = 120
    camera.follow(player.position, (128 - 48, 96 - 32))

    player.force += (0, -100 * player.mass)

    if not player.can_jump:
        speed /= 2

    v = player.velocity
    if pyxel.btn(pyxel.KEY_RIGHT):
        v = v.copy(x=+speed)
    elif pyxel.btn(pyxel.KEY_LEFT):
        v = v.copy(x=-speed)
    elif player.can_jump and not pyxel.btnp(pyxel.KEY_UP):
        v = Vec2d(v.x * 0.5, v.y)

    if player.can_jump and pyxel.btnp(pyxel.KEY_UP):
        v = v.copy(x=2 * v.x, y=jump)
        player.can_jump = False
    player.velocity = v


space.run()
