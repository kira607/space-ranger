import typing as t

import numpy as np
import pygame as pg

from ._base import Property

_TValue: t.TypeAlias = pg.Color
_TInput: t.TypeAlias = pg.Color | tuple[int, int, int, int] | tuple[int, int, int] | int


class Color(Property[_TValue, _TInput]):
    """A color property.

    :param default: Initial value, defaults to black (`pygame.Color(0, 0, 0, 255)`).
    :type default: _TInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(self, default: InputType = 0) -> None:
        super().__init__(default)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        if isinstance(value, cls.ValueType):
            return value
        if isinstance(value, int):
            return pg.Color(value, value, value)
        return pg.Color(*value)

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        return np.array((value.r, value.g, value.b, value.a))

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        r, g, b, a = array.clip(0, 255).astype(int).tolist()
        return pg.Color(r, g, b, a)
