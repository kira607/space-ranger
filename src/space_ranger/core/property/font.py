import typing as t
from pathlib import Path

import numpy as np

from space_ranger.core.asset import FontAsset, FontFactory

from ._property import Property


_TValue: t.TypeAlias = FontFactory
_TInput: t.TypeAlias = FontFactory | FontAsset | Path | str | None


class Font(Property[_TValue, _TInput]):
    """A font property.

    :param default: Initial value, defaults to None.
    :type default: _TFontInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(self, default: InputType = None) -> None:
        super().__init__(default)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        if value is None:
            return FontFactory(None)
        if isinstance(value, Path | str):
            return FontAsset(value).load()
        return value

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        raise NotImplementedError()

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        raise NotImplementedError()
