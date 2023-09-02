from pygame import Vector2

from ._game_object_property import GameObjectProperty


class Position(GameObjectProperty[Vector2]):
    """A position game object property.

    Represents a position of a game object on a screen.

    :param Vector2 default: The default position, defaults to Vector(0, 0).
    """

    __animatable__ = True
    __default__ = Vector2(0, 0)
