import typing as t

import numpy as np
import pygame as pg

from ._property import Property


_TValue: t.TypeAlias = pg.math.Vector2
_TInput: t.TypeAlias = pg.math.Vector2, tuple[int | float, int | float]


class Vector2(Property[_TValue, _TInput]):
    """A vector2 property.

    :param default: Initial value, defaults to (0, 0).
    :type default: _TIntInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(
        self,
        default: InputType = (0, 0),
    ) -> None:
        super().__init__(default)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        if isinstance(value, pg.Vector2):
            return value
        if isinstance(value, tuple) and len(value) == 2:
            return pg.Vector2(value[0], value[1])
        return None

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        return value

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        return array
