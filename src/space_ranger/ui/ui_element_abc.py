from abc import ABC, abstractmethod

import pygame


class UIElementABC(ABC):
    """UI element interface."""

    # Element properties

    @property
    @abstractmethod
    def position(self) -> pygame.Vector2:
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
