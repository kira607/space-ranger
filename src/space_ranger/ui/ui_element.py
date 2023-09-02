from abc import ABC

from pygame import Vector2

from space_ranger.common import TPosition

from .ui_element_abc import UIElementABC


class UIElement(UIElementABC, ABC):
    """A base UI element."""

    def __init__(self, position: TPosition = (0, 0)) -> None:
        self._position: Vector2
        self._set_position(position)

    # Element properties

    @property
    def position(self) -> Vector2:
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
        if isinstance(position, Vector2):
            self._position = position
        else:
            self._position = Vector2(*position)

    def _update_position(self) -> None:  # noqa: B027
        """Update element position."""
        pass
