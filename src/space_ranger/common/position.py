from __future__ import annotations

import inspect
from collections import namedtuple
from typing import Any, Union

PositionValue = int | float
PositionTuple = tuple[PositionValue, PositionValue]
PositionOperand = Union[int, float, PositionTuple, "Position"]


class Position(namedtuple("Position", ["x", "y"])):
    """A position object."""

    __slots__ = ()

    def __truediv__(self, other: int | float) -> Position:
        """Divide position by x and y."""
        return Position(self.x / other, self.y / other)

    def __add__(self, other: PositionOperand) -> Position:  # type: ignore
        """Add position to position or int to position.

        :param int | Position other: A postioin or int to add.

        :raises ValueError: other has incompatible type.

        :return: A new position.
        :rtype: Position
        """
        if isinstance(other, (int, float)):
            return Position(self.x + other, self.y + other)
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        raise ValueError(
            f"{inspect.stack()[0][3]} is not supported between "
            f"{self.__class__.__name__} and {type(other).__name__}",
        )

    def __sub__(self, other: PositionOperand) -> Position:
        """Subtract position from position or int from position.

        :param int | Position other: A postioin or int to subtract.

        :raises ValueError: other has incompatible type.

        :return: A new position.
        :rtype: Position
        """
        if isinstance(other, int):
            return Position(self.x - other, self.y - other)
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x - other[0], self.y - other[1])
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        raise ValueError(
            f"{inspect.stack()[0][3]} is not supported between "
            f"{self.__class__.__name__} and {type(other).__name__}",
        )


TPosition = PositionTuple | Position


def is_position(obj: Any, raise_error: bool = False) -> bool:
    """Get if value is a :class:`space_ranger.common.Position` compatible object.

    :param Any obj: object to check
    :param bool raise_error: Raise an exception if obj is
      not a :class:`space_ranger.common.Position` compatible.

    :raise ValueError: obj is not a :class:`space_ranger.common.Position` compatible.

    :return: bool: True if value is a :class:`space_ranger.common.Position`
      compatible object, False otherwise.
    :rtype: bool
    """
    compatible = any(
        (
            isinstance(obj, Position),
            all(
                (
                    isinstance(obj, tuple),
                    len(obj) == 2,
                    isinstance(obj[0], (int, float)),
                    isinstance(obj[1], (int, float)),
                ),
            ),
        ),
    )

    if not compatible and raise_error:
        raise ValueError("obj is not a Position")

    return compatible
