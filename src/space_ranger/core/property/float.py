import typing as t

import numpy as np
import pygame as pg

from ._property import Property


_TValue: t.TypeAlias = float
_TInput: t.TypeAlias = int | float


class Float(Property[_TValue, _TInput]):
    """A float property.

    :param default: Initial value, defaults to 0.0.
    :type default: _TFloatInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(
        self,
        default: InputType = 0.0,
        readonly: bool = False,
        track: bool = True,
    ) -> None:
        super().__init__(default, readonly, track)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        value = float(value)
        if cls.lowest is None:
            if cls.highest is None:
                return value
            return min(value, cls.highest)
        if cls.highest is None:
            return max(value, cls.lowest)
        return float(pg.math.clamp(value, cls.lowest, cls.highest))

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        return value

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        return array
