import pygame as pg

from space_ranger.core.game_object_property import Color, Font, Int
from space_ranger.core.game_object_property import Text as TextProperty

from ._game_object import GameObject


class Text(GameObject):
    """A plain text that can be shown on the screen."""

    text = TextProperty()
    color = Color()
    size = Int()
    font = Font()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._img = None

    @property
    def width(self) -> int:
        """Get text width."""
        return self._img.get_width()

    @property
    def height(self) -> int:
        """Get text height."""
        return self._img.get_height()

    def build(self) -> None:
        """Build the Text."""
        self.font.resize(self.size.value)
        self._img = self.font.value.render(self.text.value, False, self.color.value)

    def draw(self, screen: pg.Surface) -> None:
        """Draw text on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.blit(self._img, self.position.value)
