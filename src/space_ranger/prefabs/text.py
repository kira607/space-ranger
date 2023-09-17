from space_ranger.core import GameObject
from space_ranger.core.property import Color, Font, Int, String


class Text(GameObject):
    """Text."""

    string = String("Text")
    font = Font()
    size = Int(20)
    color = Color(255)

    @property
    def width(self) -> int:
        """Get text widht."""
        return self.image.get_width()

    @property
    def height(self) -> int:
        """Get text height."""
        return self.image.get_height()

    def _build(self) -> None:
        self.image = self.font(self.size).render(self.string, True, self.color)
