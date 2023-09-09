from space_ranger.core import Property


class Int(Property[int]):
    """An int game object property.

    Holds an integer value.

    :param int default: The default value, defaults to 0.
    """

    __animatable__ = True
    __default__ = 0
