import pygame as pg

from ._game_object_property import GameObjectProperty


class Color(GameObjectProperty[pg.Color]):
    """A color game object property.

    Holds a pygame.Color value.

    :param pygame.Color default: The default color, defaults to pygame.Color(0, 0, 0, 255).
    """

    __animatable__ = False
    __default__ = pg.Color(0, 0, 0, 255)
