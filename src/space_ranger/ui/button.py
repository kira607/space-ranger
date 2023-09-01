from abc import ABC

import pygame

from space_ranger.common import BLACK, GREY, Color, TPosition

from .text import Text
from .ui_element import UIElement


class _ButtonText(Text):
    """Button text class."""

    def on_hover(self) -> None:
        """Do nothing."""
        pass


class Button(UIElement, ABC):
    """A menu button.

    :param TPosition, optional position: Button position, defaults to (0, 0)
    :param Color, optional color: Button color, defaults to Color.GREY
    :param str, optional text: Button text string. Can be either a string or a Text object. defaults to "Button"
    :param Color, optional text_color: Button text color, defaults to Color.BLACK
    :param pygame.font.Font | None, optional text_font: Button text font, defaults to None
    """

    def __init__(
        self,
        position: TPosition = (0, 0),
        *,
        color: Color = GREY,
        text: str = "Button",
        text_color: Color = BLACK,
        text_font: pygame.font.Font | None = None,
    ) -> None:
        super().__init__(position)
        self._text = _ButtonText(text=text, color=text_color, font=text_font)
        self._color = color
        self._rect = pygame.Rect(
            *self.position,
            self._text.width * 1.3,
            self._text.height * 1.6,
        )
        self._update_position()

    # Element properties

    @property
    def width(self) -> int:
        """Get button width."""
        return self._rect.width

    @property
    def height(self) -> int:
        """Get button height."""
        return self._rect.height

    # Button properties

    @property
    def text(self) -> str:
        """Button text string."""
        return self._text.text

    @text.setter
    def text(self, text: str) -> None:
        """Set button text."""
        self._text.text = text

    @property
    def text_color(self) -> Color:
        """Button text color."""
        return self._text.color

    @text_color.setter
    def text_color(self, color: Color) -> None:
        """Set button text color."""
        self._text.color = color

    @property
    def text_font(self) -> pygame.font.Font:
        """Button text font."""
        return self._text.font

    @text_font.setter
    def text_font(self, font: pygame.font.Font) -> None:
        """Set button text font."""
        self._text.font = font

    @property
    def color(self) -> Color:
        """Button color."""
        return self._color

    @color.setter
    def color(self, color: Color) -> None:
        """Set button color."""
        self._color = color

    # Public methods

    def draw(self, screen: pygame.Surface) -> None:
        """Draw a buttion on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        pygame.draw.rect(screen, self._color, self._rect)
        self._text.draw(screen)

    # Helpers?

    def _update_position(self) -> None:
        self._rect = pygame.Rect(*self.position, self.width, self.height)
        self._text.position = (
            self.position.x + self.width / 2 - self._text.width / 2,
            self.position.y + self.height / 2 - self._text.height / 2,
        )
