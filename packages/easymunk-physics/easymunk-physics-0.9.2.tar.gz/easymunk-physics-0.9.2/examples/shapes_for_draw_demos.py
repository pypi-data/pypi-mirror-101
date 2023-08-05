""" Helper function fill_space for the draw demos. 
Adds a lot of stuff to a space.
"""

import easymunk


def fill_space(space, custom_color=(255, 255, 0, 255)):
    captions = []

    # Static
    captions.append(((50, 680), "Static Shapes"))

    # Static Segments
    segments = [
        easymunk.Segment((10, 400), (10, 600), 0, space.static_body),
        easymunk.Segment((20, 400), (20, 600), 1, space.static_body),
        easymunk.Segment((30, 400), (30, 600), 3, space.static_body),
        easymunk.Segment((50, 400), (50, 600), 5, space.static_body),
    ]
    space.add(*segments)

    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (40, 630)
    b.angle = 3.14 / 7
    s = easymunk.Segment((-30, 0), (30, 0), 2, b)
    space.add(b, s)

    # Static Circles
    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (120, 630)
    s = easymunk.Circle(10, body=b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (120, 630)
    s = easymunk.Circle(10, (-30, 0), b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (120, 560)
    b.angle = 3.14 / 4
    s = easymunk.Circle(40, body=b)
    space.add(b, s)

    # Static Polys
    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (120, 460)
    b.angle = 3.14 / 4
    s = easymunk.Poly([(0, -25), (30, 25), (-30, 25)], body=b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (120, 500)
    t = easymunk.Transform(ty=-100)
    s = easymunk.Poly([(0, -25), (30, 25), (-30, 25)], radius=1, body=b, transform=t)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (50, 430)
    t = easymunk.Transform(ty=-100)
    s = easymunk.Poly(
        [
            (0.0, -30.0),
            (19.0, -23.0),
            (30.0, -5.0),
            (26.0, 15.0),
            (10.0, 28.0),
            (-10.0, 28.0),
            (-26.0, 15.0),
            (-30.0, -5.0),
            (-19.0, -23.0),
        ],
        body=b,
        transform=t,
    )
    space.add(b, s)

    # Kinematic
    captions.append(((220, 680), "Kinematic Shapes"))

    # Kinematic Segments
    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    segments = [
        easymunk.Segment((180, 400), (180, 600), 0, b),
        easymunk.Segment((190, 400), (190, 600), 1, b),
        easymunk.Segment((200, 400), (200, 600), 3, b),
        easymunk.Segment((220, 400), (220, 600), 5, b),
    ]
    space.add(b, *segments)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (210, 630)
    b.angle = 3.14 / 7
    s = easymunk.Segment((-30, 0), (30, 0), 2, b)
    space.add(b, s)

    # Kinematic Circles
    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (290, 630)
    s = easymunk.Circle(10, body=b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (290, 630)
    s = easymunk.Circle(10, (-30, 0), b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (290, 560)
    b.angle = 3.14 / 4
    s = easymunk.Circle(40, body=b)
    space.add(b, s)

    # Kinematic Polys
    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (290, 460)
    b.angle = 3.14 / 4
    s = easymunk.Poly([(0, -25), (30, 25), (-30, 25)], body=b)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (290, 500)
    t = easymunk.Transform(ty=-100)
    s = easymunk.Poly([(0, -25), (30, 25), (-30, 25)], radius=3, body=b, transform=t)
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (230, 430)
    t = easymunk.Transform(ty=-100)
    s = easymunk.Poly(
        [
            (19.0, -50.0),
            (30.0, -5.0),
            (26.0, 15.0),
            (10.0, 38.0),
            (-10.0, 38.0),
            (-26.0, 15.0),
            (-30.0, -5.0),
            (-19.0, -50.0),
        ],
        body=b,
        transform=t,
    )
    space.add(b, s)

    # Dynamic
    captions.append(((390, 680), "Dynamic Shapes"))

    # Dynamic Segments
    b = easymunk.Body(1, 1)
    segments = [
        easymunk.Segment((350, 400), (350, 600), 0, b),
        easymunk.Segment((360, 400), (360, 600), 1, b),
        easymunk.Segment((370, 400), (370, 600), 3, b),
        easymunk.Segment((390, 400), (390, 600), 5, b),
    ]
    space.add(b, *segments)

    b = easymunk.Body(1, 1)
    b.position = (380, 630)
    b.angle = 3.14 / 7
    s = easymunk.Segment((-30, 0), (30, 0), 7, b)
    space.add(b, s)

    # Dynamic Circles
    b = easymunk.Body(1, 1)
    b.position = (460, 630)
    s = easymunk.Circle(10, body=b)
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (460, 630)
    s = easymunk.Circle(10, (-30, 0), b)
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (460, 560)
    b.angle = 3.14 / 4
    s = easymunk.Circle(40, body=b)
    space.add(b, s)

    # Dynamic Polys

    b = easymunk.Body(1, 1)
    b.position = (460, 460)
    b.angle = 3.14 / 4
    s = easymunk.Poly([(0, -25), (30, 25), (-30, 25)], body=b)
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (460, 500)
    s = easymunk.Poly(
        [(0, -25), (30, 25), (-30, 25)],
        radius=5,
        body=b,
        transform=easymunk.Transform(ty=-100),
    )
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (400, 430)
    s = easymunk.Poly(
        [(0, -50), (50, 0), (30, 50), (-30, 50), (-50, 0)],
        body=b,
        transform=easymunk.Transform(ty=-100),
    )
    space.add(b, s)

    # Constraints

    # PinJoints
    captions.append(((560, 660), "Pin Joint"))
    a = easymunk.Body(1, 1)
    a.position = (550, 600)
    easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (650, 620)
    easymunk.Circle(20, body=b)
    j = easymunk.DistanceJoint(a, b, anchor_a=(0, 0), anchor_b=(0, -20))
    space.add(a, b, j)

    # SlideJoints
    captions.append(((560, 560), "Slide Joint"))
    a = easymunk.Body(1, 1)
    a.position = (550, 500)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (650, 520)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.LimitDistanceJoint(
        a, b, min=10, max=30, anchor_a=(0, 20), anchor_b=(0, -20)
    )
    space.add(a, b, j)

    # PivotJoints
    captions.append(((560, 460), "Pivot Joint"))
    a = easymunk.Body(1, 1)
    a.position = (550, 400)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (650, 420)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.PositionJoint(a, b, (600, 390))
    space.add(a, b, j)

    # GrooveJoints
    captions.append(((760, 660), "Groove Joint"))
    a = easymunk.Body(1, 1)
    a.position = (750, 600)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (850, 620)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.SegmentJoint(a, b, (40, 40), (40, -40), (-60, 0))
    space.add(a, b, j)

    # DampedSpring
    captions.append(((760, 550), "Damped Spring"))
    a = easymunk.Body(1, 1)
    a.position = (750, 480)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (850, 500)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.DampedSpring(a, b, 1, 1, 100, (0, 0), (0, 10))
    space.add(a, b, j)

    # DampedRotarySpring
    captions.append(((740, 430), "Damped Rotary Spring"))
    a = easymunk.Body(1, 1)
    a.position = (750, 350)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (850, 380)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.DampedRotarySpring(a, b, 1, 1, 10)
    space.add(a, b, j)

    # RotaryLimitJoint
    captions.append(((740, 300), "Rotary Limit Joint"))
    a = easymunk.Body(1, 1)
    a.position = (750, 220)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (850, 250)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.LimitAngleJoint(a, b, 1, 2)
    b.angle = 3
    space.add(a, b, j)

    # RatchetJoint
    captions.append(((740, 170), "Ratchet Joint"))
    a = easymunk.Body(1, 1)
    a.position = (750, 100)
    sa = easymunk.Circle(20, body=a)
    b = easymunk.Body(1, 1)
    b.position = (850, 120)
    sb = easymunk.Circle(20, body=b)
    j = easymunk.RatchetJoint(a, b, 0.1, 1)
    b.angle = 3
    space.add(a, b, j)

    # GearJoint and SimpleMotor omitted since they are similar to the already
    # added joints

    # TODO: more stuff here :)

    # Other

    # Objects in custom color
    captions.append(((150, 150), "Custom Color (static, kinematic & dynamic)"))
    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (200, 200)
    s = easymunk.Circle(30, body=b)
    s.color = custom_color
    space.add(b, s)

    b = easymunk.Body(body_type=easymunk.Body.KINEMATIC)
    b.position = (300, 200)
    s = easymunk.Circle(30, body=b)
    s.color = custom_color
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (400, 200)
    s = easymunk.Circle(30, body=b)
    s.color = custom_color
    space.add(b, s)

    # Collision
    captions.append(((550, 150), "Collisions"))
    b = easymunk.Body(body_type=easymunk.Body.STATIC)
    b.position = (570, 200)
    s = easymunk.Circle(40, body=b)
    space.add(b, s)

    b = easymunk.Body(1, 1)
    b.position = (590, 250)
    s = easymunk.Circle(40, body=b)
    space.add(b, s)

    # Sleeping
    captions.append(((50, 150), "Sleeping"))
    b = easymunk.Body(1, 1)
    b.position = (75, 200)
    space.sleep_time_threshold = 0.01
    s = easymunk.Circle(40, body=b)
    space.add(b)
    b.sleep()
    space.step(0.000001)

    return captions


def main():
    space = easymunk.Space()
    fill_space(space)

    options = easymunk.DrawOptions()
    space.step(1)
    space.step(2)
    space.debug_draw(options)


if __name__ == "__main__":
    import sys

    sys.exit(main())
