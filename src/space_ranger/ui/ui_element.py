from abc import ABC

from space_ranger.common import Position, TPosition, is_position

from .ui_element_abc import UIElementABC


class UIElement(UIElementABC, ABC):
    """A base UI element."""

    def __init__(self, position: TPosition = (0, 0)) -> None:
        self._position: Position
        self._set_position(position)

    # Element properties

    @property
    def position(self) -> Position:
        """The position of the element."""
        return self._position

    @position.setter
    def position(self, position: TPosition) -> None:
        """Set an element position.

        :param Position position: New element position.
        """
        self._set_position(position)
        self._update_position()

    # Helpers?

    def _set_position(self, position: TPosition) -> None:
        """Set element position."""
        if is_position(position):
            position = Position(position[0], position[1])
            self._position = position

    def _update_position(self) -> None:  # noqa: B027
        """Update element position."""
        pass
