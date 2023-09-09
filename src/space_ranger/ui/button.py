import pygame as pg

from space_ranger.asset import FontFactory
from space_ranger.property import Color, Font, Int
from space_ranger.property import Text as TextProp

from .text import Text
from .ui_element import UIElement


class _ButtonBackground(pg.sprite.Sprite):
    """A button background.

    :param int x: x coordinate of the backgroud.
    :param int y: y coordinate of the backgroud.
    :param int width: Width of the button.
    :param int height: Height of the button.
    :param pg.Color color: Backgroud color.
    """

    def __init__(self, x: int, y: int, width: int, height: int, color: pg.Color) -> None:
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Button(UIElement):
    """A simple button.

    :param FontFactory, optional text_font: A font factory for button text font, defaults to None
    :param pg.Vector2 | None, optional position: Button position, defaults to None
        if None, a position will be at (0, 0)
    :param str, optional text: Button text, defaults to "Button"
    :param pg.Color, optional text_color: Button text color, defaults to WHITE
    :param int, optional text_size: Button text size, defaults to 16
    :param pg.Color, optional color: Button color, defaults to BLACK
    """

    text = TextProp()
    text_color = Color()
    text_size = Int()
    text_font = Font()
    color = Color()

    def __init__(
        self,
        position: pg.Vector2 | None = None,
        *,
        text: str | None = None,
        text_color: pg.Color | None = None,
        text_size: int | None = None,
        text_font: FontFactory | None = None,
        color: pg.Color | None = None,
    ) -> None:
        super().__init__(position)
        self.text.set_value(text)
        self.text_color.set_value(text_color)
        self.text_size.set_value(text_size)
        self.text_font.set_value(text_font)
        self.color.set_value(color)
        self._back: pg.sprite.GroupSingle
        self._text: Text

    @property
    def width(self) -> int:
        """Get button width."""
        return self._back.sprite.rect.width

    @property
    def height(self) -> int:
        """Get button height."""
        return self._back.sprite.rect.height

    def build(self) -> None:
        """Build the Button."""
        self._text = Text(
            text=self.text.value,
            font=self.text_font.value,
            size=self.text_size.value,
            color=self.text_color.value,
        )
        self._text.build()
        self._back = pg.sprite.GroupSingle(
            _ButtonBackground(
                self.position.value.x,
                self.position.value.y,
                self._text.width * 1.3,
                self._text.height * 1.6,
                self.color.value,
            ),
        )
        self._text.position = pg.Vector2(
            self.position.value.x + self.width / 2 - self._text.width / 2,
            self.position.value.y + self.height / 2 - self._text.height / 2,
        )

    def draw(self, screen: pg.Surface) -> None:
        """Draw text on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        self._back.draw(screen)
        self._text.draw(screen)
