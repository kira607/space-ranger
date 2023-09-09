import pygame as pg

from space_ranger.asset import FontFactory
from space_ranger.property import Color, Font, Int
from space_ranger.property import Text as TextProp

from .ui_element import UIElement


class _TextSprite(pg.sprite.Sprite):
    """A text game object sprite."""

    def __init__(self, text: str, font: pg.font.Font, color: pg.Color, pos: pg.Vector2) -> None:
        super().__init__()
        self.image: pg.Surface = font.render(text, False, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos.x, pos.y)


class Text(UIElement):
    """A plain text that can be shown on the screen.

    :param pg.Vector2 | None, optional position: Text position, defaults to None.
      When None a positon will be (0, 0)
    :param str, optional text: Text string, defaults to "Text"
    :param str, optional color: Text color, defaults to BLACK
    :param int, optional size: Text size, defaults to 16
    :param FontFactory | None, optional font: Text font, defaults to None
    """

    text = TextProp()
    color = Color()
    size = Int()
    font = Font()

    def __init__(
        self,
        position: pg.Vector2 | None = None,
        *,
        text: str | None = None,
        color: pg.Color | None = None,
        size: int | None = None,
        font: FontFactory | None = None,
    ) -> None:
        super().__init__(position)
        self.text.set_value(text)
        self.color.set_value(color)
        self.size.set_value(size)
        self.font.set_value(font)
        self._text_sprite: pg.sprite.GroupSingle

    @property
    def width(self) -> int:
        """Get text width."""
        return self._text_sprite.sprite.image.get_width()

    @property
    def height(self) -> int:
        """Get text height."""
        return self._text_sprite.sprite.image.get_height()

    def build(self) -> None:
        """Build the Text."""
        for p in self.__children__:
            print(f"{p.name}={p.value}")

        self._text_sprite = pg.sprite.GroupSingle(
            _TextSprite(
                self.text.value,
                self.font.value(self.size.value),
                self.color.value,
                self.position.value,
            ),
        )

    def draw(self, screen: pg.Surface) -> None:
        """Draw text on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        self._text_sprite.draw(screen)
