import typing as t

import numpy as np

from ._property import Property

_TValue: t.TypeAlias = str
_TInput: t.TypeAlias = str | bytes | t.Any


class String(Property[_TValue, _TInput]):
    """An string property.

    :param default: Initial value, defaults to "".
    :type default: _TInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(self, default: InputType = "") -> None:
        super().__init__(default)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        return str(value)

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        raise NotImplementedError()

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        raise NotImplementedError()
