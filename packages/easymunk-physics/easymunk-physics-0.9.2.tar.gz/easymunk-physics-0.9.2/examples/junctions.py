import pyxel

from easymunk import pyxel as phys

pyxel.init(256, 196)
space = phys.space(camera=phys.Camera(flip_y=True), damping=0.9)

coords = (20, 20, 80, 20, 50, 70)
a = phys.tri(*coords, color=pyxel.COLOR_RED).move(20, 30)
b = phys.tri(*coords, color=pyxel.COLOR_YELLOW).move(150, 100)
a_initial_position = a.position
b_initial_position = b.position

phys.margin()
junction = a.junction(b)
space.shapes.apply(friction=0.75)
paused = False
text = "..."


@space.before_step("generator")
def _():
    global text

    # Define durations
    SHORT_INTERVAL = range(60)
    LONG_INTERVAL = range(120)
    VERY_LONG_INTERVAL = range(240)

    # b.boost(-10, 10).pin_to_segment((-20, 0), (20, 0), ratio=0.5)
    g = 200
    # spac
    # e.gravity = (0, -100)
    L = 50
    space.damping = 1
    a.angular_velocity = 60
    a.moment = 1
    a.rotary_spring(2, 1)
    return

    # Start animation
    text = "A and B are not connected now."
    yield from SHORT_INTERVAL

    text = "We connect them with a gear.\nThe phase angle of 30deg imposes a rotation."
    junction.fix_rotation_ratio(1, 30)
    yield from LONG_INTERVAL

    text = "Now we flip connection, \nwhich inverts the phase angle."
    junction.clear().flipped.fix_rotation_ratio(1, 30)
    yield from LONG_INTERVAL

    text = "We add a counterclockwise motor to body A.\nNotice that B also flips."
    m = a.fix_angular_velocity(60)
    yield from VERY_LONG_INTERVAL

    text = "We clear joints and add a pivot."
    m.detach()
    junction.clear().fix_position((a.position + b.position) / 2)
    j2 = b.pin_position()
    yield from SHORT_INTERVAL

    text = "Let us turn on gravity!"
    space.gravity = (0, -200)
    yield from SHORT_INTERVAL

    j2.detach()
    junction.clear_all()
    yield from LONG_INTERVAL

    text = "Clear!"
    j1 = a.pin_position(a_initial_position, world=True)
    j2 = b.pin_position(b_initial_position, world=True)
    space.gravity = (0, 0)
    yield from LONG_INTERVAL
    j1.detach()
    j2.detach()

    text = "Now let us connect objects with \na string with variable length."
    b.pin_position()
    junction.fix_distance(distance=(0, 100))
    yield from LONG_INTERVAL

    text = "This is a fixed_distance() constraint."
    space.gravity = (0, -100)
    yield from LONG_INTERVAL

    text = "It does not constrain angular variables."
    m = a.fix_angular_velocity(120)
    yield from LONG_INTERVAL

    text = "Now we connect them with a ratchet"
    junction.ratchet(-30)
    m.rate *= -1
    yield from LONG_INTERVAL

    text = "See what happens when we flip the rotation\nof A a few times."
    for _ in range(4):
        m.rate *= -1
        yield from SHORT_INTERVAL

        m.rate *= -1
        yield from SHORT_INTERVAL

    text = "Now we move the motor to B"
    m.detach()
    m = b.fix_angular_velocity(120)
    yield from LONG_INTERVAL

    text = "We flip rotations again..."
    for _ in range(4):
        m.rate *= -1
        yield from SHORT_INTERVAL

        m.rate *= -1

    text = "Thats all folks!"
    m.detach()
    junction.clear_all()
    yield from VERY_LONG_INTERVAL


@space.after_step()
def _():
    # Print main message
    pyxel.text(10, 10, text, pyxel.COLOR_WHITE)

    # Show legend in the top-right corner
    width = 6 * pyxel.FONT_WIDTH
    height = 2 * pyxel.FONT_HEIGHT
    x = pyxel.width - 10 - width
    y1 = 10
    y2 = y1 + pyxel.FONT_HEIGHT
    pyxel.rectb(x - 3, y1 - 3, 6 + width, 6 + height, pyxel.COLOR_WHITE)
    pyxel.text(x, y1, "Body A", a.color)
    pyxel.text(x, y2, "Body B", b.color)

    # Show body names and angles
    err = -3.5 * pyxel.FONT_WIDTH, -pyxel.FONT_HEIGHT / 2
    space.camera.text(*(a.position + err), f"A:{a.angle:+1.0f}deg", 0)
    space.camera.text(*(b.position + err), f"B:{b.angle:+1.0f}deg", 0)


def update():
    global paused
    if pyxel.btnp(pyxel.KEY_SPACE):
        paused = not paused
    if not paused:
        space.update()


def draw():
    space.draw(clear=True)


pyxel.run(update, draw)
