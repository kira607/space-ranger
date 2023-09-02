from ._game_object_property import GameObjectProperty


class Text(GameObjectProperty[str]):
    """A text game object property.

    Holds a text string.

    :param str default: The default string, defaults to "Text".
    """

    __animatable__ = False
    __default__ = "Text"
