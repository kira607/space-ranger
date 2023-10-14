import typing as t

import numpy as np

from ._property import Property

_TValue: t.TypeAlias = bool
_TInput: t.TypeAlias = t.Any


class Bool(Property[_TValue, _TInput]):
    """A boolean property.

    :param default: Initial value, defaults to False.
    :type default: _TInput
    """

    ValueType: t.TypeAlias = _TValue
    InputType: t.TypeAlias = _TInput

    def __init__(self, default: InputType = False) -> None:
        super().__init__(default)

    @classmethod
    def adapt(cls, value: InputType) -> ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        return bool(value)

    @classmethod
    def to_array(cls, value: ValueType) -> np.ndarray:
        """Convert value to a numpy array."""
        raise NotImplementedError()

    @classmethod
    def from_array(cls, array: np.ndarray) -> ValueType:
        """Convert a numpy array to value."""
        raise NotImplementedError()
