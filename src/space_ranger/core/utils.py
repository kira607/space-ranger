from __future__ import annotations

import typing as t

import pygame as pg


class _Missing:
    """Explicit missing class."""

    __slots__ = ()

    def __bool__(self) -> bool:
        """Get bool value."""
        return False

    def __copy__(self) -> _Missing:
        """Get copy."""
        return self

    def __deepcopy__(self) -> _Missing:
        """Get deep copy."""
        return self

    def __str__(self) -> str:
        """Get string representation."""
        return "MISSING"

    def __repr__(self) -> str:
        """Get object representation."""
        return f"<{str(self)}>"


MISSING = _Missing()


type ColorType = pg.color.Color | tuple[int, int, int] | tuple[int, int, int, int] | str
type Bool = bool | t.Literal[0, 1]
type Alignment = t.Literal["left", "center", "right"]


def get_text_surface(
    *lines: str,
    font: pg.font.Font,
    color: ColorType = (255, 255, 255),
    background: ColorType = (0, 0, 0, 255),
    antialias: Bool = False,
    alignment: Alignment = "left",
) -> pg.Surface:
    """Get a text surface for multiline text.

    :param font: Text font.
    :type font: pg.font.Font
    :param color: Text color, defaults to (255, 255, 255)
    :type color: ColorType, optional
    :param background: Text background color, defaults to (0, 0, 0, 255)
    :type background: ColorType, optional

    :return: A single surface with given text lines blited on that.
    :rtype: pg.Surface
    """
    lines_surfaces = [font.render(line, antialias, color) for line in lines]
    width = max([line_surface.get_width() for line_surface in lines_surfaces])
    height = sum([line_surface.get_height() for line_surface in lines_surfaces])
    result_surface = pg.Surface((width, height), pg.SRCALPHA)
    result_surface.fill(background)
    prev_height = 0
    for line_surface in lines_surfaces:
        match alignment:
            case "left":
                x = 0
            case "center":
                x = width // 2 - line_surface.get_width() // 2
            case "right":
                x = width - line_surface.get_width()
            case _:
                raise ValueError(f"Invalid alignment value: {alignment}")
        result_surface.blit(line_surface, (x, prev_height))
        prev_height += line_surface.get_height()
    return result_surface


def draw_arrow(
    surface: pg.Surface,
    pos: pg.math.Vector2,
    vec: pg.math.Vector2,
    color: pg.Color = "white",
    width: int = 1,
    arrow_line_length: int = 10,
    arrow_line_angle: int = 30,
) -> None:
    """Draw a vector arrow on a surface.

    :param surface: A surface to draw on.
    :type surface: pg.Surface
    :param pos: Start position of the vector.
    :type pos: pg.math.Vector2
    :param vec: The vector to draw
    :type vec: pg.math.Vector2
    :param color: Arrow color, defaults to "black"
    :type color: pg.Color, optional
    :param width: Thickness of arrow lines, defaults to 1
    :type width: int, optional
    :param arrow_line_length: Lenght of arrow tip lines, defaults to 10
    :type arrow_line_length: int, optional
    :param arrow_line_angle: Angle of arrow tip lines in degrees, defaults to 30
    :type arrow_line_angle: int, optional
    """
    if vec == (0, 0):
        return

    arrow_tip = pos + vec

    arrow_line_1 = -vec
    arrow_line_1.normalize_ip()
    arrow_line_1.rotate_ip(-arrow_line_angle)
    arrow_line_1 *= arrow_line_length

    arrow_line_2 = -vec
    arrow_line_2.normalize_ip()
    arrow_line_2.rotate_ip(arrow_line_angle)
    arrow_line_2 *= arrow_line_length

    pg.draw.line(surface, color, pos, arrow_tip, width=width)
    pg.draw.line(surface, color, arrow_tip, arrow_tip + arrow_line_1, width=width)
    pg.draw.line(surface, color, arrow_tip, arrow_tip + arrow_line_2, width=width)


_DEFAULT_COLOR = pg.color.Color(0, 0, 0)


def rect(width: int, height: int, color: pg.color.Color = _DEFAULT_COLOR) -> pg.Surface:
    """Get a rectangle sprite image.

    :param width: Width of the rectangle.
    :type width: int
    :param height: Height of the rectangle.
    :type height: int
    :param color: Rectangle fill color, defaults to _DEFAULT_COLOR
    :type color: pg.color.Color, optional

    :return: A pygame Surface with a rectangle with given parameters.
    :rtype: pg.Surface
    """
    surf = pg.Surface((width, height), pg.SRCALPHA)
    surf.fill(color)
    return surf


def circle(radius: int, color: pg.color.Color = _DEFAULT_COLOR) -> pg.Surface:
    """Get a circle sprite image.

    :param radius: Circle radius.
    :type radius: int
    :param color: Circle fill color, defaults to _DEFAULT_COLOR
    :type color: pg.color.Color, optional

    :return: A pygame Surface with a circle with given parameters.
    :rtype: pg.Surface
    """
    diameter = radius * 2
    surf = pg.Surface((diameter, diameter), pg.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    pg.draw.circle(surf, color, (radius, radius), radius)
    return surf


def square(size: int, color: pg.color.Color = _DEFAULT_COLOR) -> pg.Surface:
    """Get a square sprite image.

    :param size: Square size.
    :type size: int
    :param color: Square fill color, defaults to _DEFAULT_COLOR
    :type color: pg.color.Color, optional

    :return: A pygame Surface with a square with given parameters.
    :rtype: pg.Surface
    """
    return rect(size, size, color)
