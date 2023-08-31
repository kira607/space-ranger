from abc import ABC, abstractmethod

import pygame

from space_ranger.common import Position


class UIElementABC(ABC):
    """UI element interface."""

    # Element properties

    @property
    @abstractmethod
    def position(self) -> Position:
        """The position of the element."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def width(self) -> int:
        """Get the width of the element."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def height(self) -> int:
        """Get the height of the element."""
        raise NotImplementedError()

    # Public methods

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw UIElement on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        raise NotImplementedError()
