import pygame as pg

from space_ranger.core import Property


class Position(Property[pg.Vector2]):
    """A position game object property.

    Represents a position of a game object on a screen.

    :param Vector2 default: The default position, defaults to Vector(0, 0).
    """

    __animatable__ = True
    __default__ = pg.Vector2(0, 0)
