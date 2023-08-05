"""
Parse SVG paths and extensions

Code adapted from `svg.path`_ by Lennart Regebro.

_svg.path: https://pypi.org/project/svg.path/
"""
import re
from typing import NamedTuple
from ..linalg import Vec2d

COMMANDS = set("MmZzLlHhVvCcSsQqTtAa")
UPPERCASE = set("MZLHVCSQTA")

COMMAND_RE = re.compile(r"([MmZzLlHhVvCcSsQqTtAa])")
FLOAT_RE = re.compile(rb"^[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")


class Move(NamedTuple):
    position: Vec2d


class Line(NamedTuple):
    start: Vec2d
    end: Vec2d


class Close(NamedTuple):
    start: Vec2d
    end: Vec2d


class CubicBezier(NamedTuple):
    start: Vec2d
    control_a: Vec2d
    control_b: Vec2d
    end: Vec2d


class QuadraticBezier(NamedTuple):
    start: Vec2d
    control: Vec2d
    end: Vec2d


class Arc(NamedTuple):
    start: Vec2d
    radius: Vec2d
    rotation: float
    arc: bool
    sweep: bool
    end: Vec2d


# The argument sequences from the grammar, made sane.
# u: Non-negative number
# s: Signed number or coordinate
# c: coordinate-pair, which is two coordinates/numbers, separated by whitespace
# f: A one character flag, doesn't need whitespace, 1 or 0
ARGUMENT_SEQUENCE = {
    "M": "c",
    "Z": "",
    "L": "c",
    "H": "s",
    "V": "s",
    "C": "ccc",
    "S": "cc",
    "Q": "cc",
    "T": "c",
    "A": "uusffc",
}


def strip_array(arg_array):
    """Strips whitespace and commas"""
    # EBNF wsp:(#x20 | #x9 | #xD | #xA) + comma: 0x2C
    while arg_array and arg_array[0] in (0x20, 0x9, 0xD, 0xA, 0x2C):
        arg_array[0:1] = b""


def pop_number(arg_array):
    res = FLOAT_RE.search(arg_array)
    if not res:
        raise ValueError(f"Expected a number, got '{arg_array}'.")
    number = float(res.group())
    start = res.start()
    end = res.end()
    arg_array[start:end] = b""
    strip_array(arg_array)

    return number


def pop_unsigned_number(arg_array):
    number = pop_number(arg_array)
    if number < 0:
        raise ValueError(f"Expected a non-negative number, got '{number}'.")
    return number


def pop_coordinate_pair(arg_array):
    x = pop_number(arg_array)
    y = pop_number(arg_array)
    return complex(x, y)


def pop_flag(arg_array):
    flag = arg_array[0]
    arg_array[0:1] = b""
    strip_array(arg_array)
    if flag == 48:  # ASCII 0
        return False
    if flag == 49:  # ASCII 1
        return True


FIELD_POPPERS = {
    "u": pop_unsigned_number,
    "s": pop_number,
    "c": pop_coordinate_pair,
    "f": pop_flag,
}


def _commandify_path(pathdef):
    """
    Splits path into commands and arguments.
    """
    token = None
    for x in COMMAND_RE.split(pathdef):
        x = x.strip()
        if x in COMMANDS:
            if token is not None:
                yield token
            if x in ("z", "Z"):
                # The end command takes no arguments, so add a blank one
                token = (x, "")
            else:
                token = (x,)
        elif x:
            if token is None:
                raise ValueError(f"Path does not start with a command: {pathdef}")
            token += (x,)
    yield token


def _tokenize_path(pathdef):
    for command, args in _commandify_path(pathdef):
        # Shortcut this for the close command, that doesn't have arguments:
        if command in ("z", "Z"):
            yield (command,)
            continue

        # For the rest of the commands, we parse the arguments and
        # yield one command per full set of arguments
        arg_sequence = ARGUMENT_SEQUENCE[command.upper()]
        arguments = bytearray(args, "ascii")
        while arguments:
            command_arguments = []
            for arg in arg_sequence:
                try:
                    command_arguments.append(FIELD_POPPERS[arg](arguments))
                except ValueError as e:
                    raise ValueError(f"Invalid path element {command} {args}") from e

            yield (command,) + tuple(command_arguments)

            # Implicit Moveto commands should be treated as Lineto commands.
            if command == "m":
                command = "l"
            elif command == "M":
                command = "L"


def parse_path(pathdef):  # noqa: C901
    segments = []
    start_pos = None
    last_command = None
    current_pos = 0

    for token in _tokenize_path(pathdef):
        command = token[0]
        absolute = command.isupper()
        command = command.upper()
        if command == "M":
            pos = token[1]
            if absolute:
                current_pos = pos
            else:
                current_pos += pos
            segments.append(Move(current_pos))
            start_pos = current_pos

        elif command == "Z":
            segments.append(Close(current_pos, start_pos))
            current_pos = start_pos

        elif command == "L":
            pos = token[1]
            if not absolute:
                pos += current_pos
            segments.append(Line(current_pos, pos))
            current_pos = pos

        elif command == "H":
            hpos = token[1]
            if not absolute:
                hpos += current_pos.real
            pos = Vec2d(hpos, current_pos.imag)
            segments.append(Line(current_pos, pos))
            current_pos = pos

        elif command == "V":
            vpos = token[1]
            if not absolute:
                vpos += current_pos.imag
            pos = Vec2d(current_pos.real, vpos)
            segments.append(Line(current_pos, pos))
            current_pos = pos

        elif command == "C":
            control1 = token[1]
            control2 = token[2]
            end = token[3]

            if not absolute:
                control1 += current_pos
                control2 += current_pos
                end += current_pos

            segments.append(CubicBezier(current_pos, control1, control2, end))
            current_pos = end

        elif command == "S":
            # Smooth curve. First control point is the "reflection" of
            # the second control point in the previous path.
            control2 = token[1]
            end = token[2]

            if not absolute:
                control2 += current_pos
                end += current_pos

            if last_command in "CS":
                # The first control point is assumed to be the reflection of
                # the second control point on the previous command relative
                # to the current point.
                control1 = current_pos + current_pos - segments[-1].control_b
            else:
                # If there is no previous command or if the previous command
                # was not an C, c, S or s, assume the first control point is
                # coincident with the current point.
                control1 = current_pos

            segments.append(CubicBezier(current_pos, control1, control2, end))
            current_pos = end

        elif command == "Q":
            control = token[1]
            end = token[2]

            if not absolute:
                control += current_pos
                end += current_pos

            segments.append(QuadraticBezier(current_pos, control, end))
            current_pos = end

        elif command == "T":
            # Smooth curve. Control point is the "reflection" of
            # the second control point in the previous path.
            end = token[1]

            if not absolute:
                end += current_pos

            if last_command in "QT":
                # The control point is assumed to be the reflection of
                # the control point on the previous command relative
                # to the current point.
                control = current_pos + current_pos - segments[-1].control
            else:
                # If there is no previous command or if the previous command
                # was not an Q, q, T or t, assume the first control point is
                # coincident with the current point.
                control = current_pos

            segments.append(QuadraticBezier(current_pos, control, end))
            current_pos = end

        elif command == "A":
            radius = Vec2d(token[1], token[2])
            rotation = token[3]
            arc = token[4]
            sweep = token[5]
            end = token[6]

            if not absolute:
                end += current_pos

            segments.append(Arc(current_pos, radius, rotation, arc, sweep, end))
            current_pos = end

        # Finish up the loop in preparation for next command
        last_command = command

    return segments
