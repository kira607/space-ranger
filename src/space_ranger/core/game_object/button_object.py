import pygame as pg

from space_ranger.core.game_object_property import Color, Font, Int
from space_ranger.core.game_object_property import Text as TextProperty

from ._game_object import GameObject
from .text_object import Text


class _ButtonBackground(pg.sprite.Sprite):
    """A button background.

    :param int x: x coordinate of the backgroud.
    :param int y: y coordinate of the backgroud.
    :param int width: Width of the button.
    :param int height: Height of the button.
    :param pg.Color color: Backgroud color.
    """

    def __init__(self, x: int, y: int, width: int, height: int, color: pg.Color) -> None:
        self.image = pg.Surface((x, y))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.width = width
        self.rect.height = height


class Button(GameObject):
    """A simple button."""

    text = TextProperty()
    text_color = Color()
    text_size = Int()
    text_font = Font()
    color = Color()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
        self._back = pg.sprite.GroupSingle(
            _ButtonBackground(
                self.position.x,
                self.position.y,
                self._text.width * 1.3,
                self._text.height * 1.6,
                self.color.value,
            ),
        )
        self._text.position = pg.Vector2(
            self.position.x + self.width / 2 - self._text.width / 2,
            self.position.y + self.height / 2 - self._text.height / 2,
        )

    def draw(self, screen: pg.Surface) -> None:
        """Draw text on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        # TODO: rewrite this draw workaround
        self._back.draw(screen)
        self._text.draw(screen)
