from types import SimpleNamespace


def echo_fn(name, *keys, function=print):
    """
    Return an echo function that receive the given positional arguments
    and execute echo_fn with a message constructed like bellow:

    >>> fn = echo_fn('fn', 'x', 'y')
    >>> fn(1, 2)
    fn(x=1, y=2)
    """

    def echo_function(*args):
        arguments = ", ".join(f"{k}={v!r}" for k, v in zip(keys, args))
        function(f"{name}({arguments})")

    return echo_function


"""
A Mock of pyxel module that simply echoes Pyxel function calls. This is useful
for debuging and testing.

>>> echo.circ(1, 2, 3, 4)
circ(x=1, y=2, r=3, col=4)
"""
echo_mod = SimpleNamespace(
    pset=echo_fn("pset", "x", "y", "col"),
    circ=echo_fn("circ", "x", "y", "r", "col"),
    circb=echo_fn("circb", "x", "y", "r", "col"),
    line=echo_fn("line", "x1", "y1", "x2", "y2", "col"),
    tri=echo_fn("tri", "x1", "y1", "x2", "y2", "x3", "y3", "col"),
    trib=echo_fn("trib", "x1", "y1", "x2", "y2", "x3", "y3", "col"),
    rect=echo_fn("rect", "x", "y", "w", "h", "col"),
    rectb=echo_fn("rectb", "x", "y", "w", "h", "col"),
    text=echo_fn("text", "x", "y", "s", "col"),
    mouse=echo_fn("mouse", "visible"),
    cls=echo_fn("cls", "col"),
    DEFAULT_PALETTE=[*range(16)],
)
