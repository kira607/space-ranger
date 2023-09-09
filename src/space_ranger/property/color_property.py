import pygame as pg

from space_ranger.core import Property


class Color(Property[pg.Color]):
    """A color game object property.

    Holds a pygame.Color value.

    :param pygame.Color default: The default color, defaults to pygame.Color(0, 0, 0, 255).
    """

    __animatable__ = True
    __default__ = pg.Color(0, 0, 0, 255)
