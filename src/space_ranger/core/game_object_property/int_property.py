from ._game_object_property import GameObjectProperty


class Int(GameObjectProperty[int]):
    """An int game object property.

    Holds an integer value.

    :param int default: The default value, defaults to 0.
    """

    __animatable__ = False
    __default__ = 0
