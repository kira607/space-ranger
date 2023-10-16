import typing as t

import pygame as pg


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
