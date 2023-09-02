from abc import ABC

import pygame

from space_ranger.common import BLACK, Color, TPosition

from .ui_element import UIElement


class Text(UIElement, ABC):
    """A text object.

    Attributes:
        position: Position of the text.
        widht: Width of the text.
        height: Height of the text.
        text: Text string.
        font: Text font.
        color: Text color.

    :param str text: A text string to display
    :param pygame.Color, optional color: Text color, defaults to Color.BLACK
    :param pygame.font.Font | None, optional font: Text font, defaults to None
    """

    def __init__(
        self,
        position: TPosition = (0, 0),
        *,
        text: str = "Text",
        color: pygame.Color = BLACK,
        font: pygame.font.Font | None = None,
    ) -> None:
        super().__init__(position)
        self._text = text
        self._color = color
        self._font = font if font else pygame.font.SysFont("Arial", 20)
        self._img: pygame.Surface
        self._update_img()
        self._update_position()

    # Element properties

    @property
    def width(self) -> int:
        """Get text width."""
        return self._img.get_width()

    @property
    def height(self) -> int:
        """Get text height."""
        return self._img.get_height()

    # Text properties

    @property
    def text(self) -> str:
        """Text string."""
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        """Set a new text."""
        self._text = new_text
        self._update_img()

    @property
    def color(self) -> pygame.Color:
        """Text color."""
        return self._color

    @color.setter
    def color(self, new_color: Color) -> None:
        """Set a new text color."""
        self._color = new_color
        self._update_img()

    @property
    def font(self) -> pygame.font.Font:
        """Text font."""
        return self._font

    @font.setter
    def font(self, new_font: pygame.font.Font) -> None:
        """Set a new text font."""
        self._font = new_font
        self._update_img()

    # Public methods

    def draw(self, screen: pygame.Surface) -> None:
        """Draw text on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.blit(self._img, self.position)

    # Helpers?

    def _update_img(self) -> None:
        """Update an uderlying pygame.Surface object for text."""
        self._img = self._font.render(self._text, False, self._color)
