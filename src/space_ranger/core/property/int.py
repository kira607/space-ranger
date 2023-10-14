import typing as t

import numpy as np
import pygame as pg

from ._property import Property

_TValue: t.TypeAlias = int
_TInput: t.TypeAlias = int | float


class Int(Property[_TValue, _TInput]):
    """An integer property.

    :param default: Initial value, defaults to 0.
    :type default: _TIntInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput
    lowest = None
    highest = None

    def __init__(
        self,
        default: InputType = 0,
        lowest: InputType | None = None,
        highest: InputType | None = None,
    ) -> None:
        super().__init__(default)
        self.lowest = lowest
        self.highest = highest

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        value = int(value)
        if cls.lowest is None:
            if cls.highest is None:
                return value
            return min(value, cls.highest)
        if cls.highest is None:
            return max(value, cls.lowest)
        return int(pg.math.clamp(value, cls.lowest, cls.highest))

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        return value

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        return array
