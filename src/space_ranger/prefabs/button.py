import pygame as pg

from space_ranger.core import GameObject
from space_ranger.core.animation import HoverAnimation
from space_ranger.core.property import Color, Font, Int, String


class Button(GameObject):
    """A button."""

    color = Color(100)
    width = Int()
    height = Int()
    text = String("Button")
    text_color = Color(170)
    text_size = Int(100)
    text_font = Font()

    def __init__(
        self,
        color: Color.InputType = 100,
        text: String.InputType = "Button",
        text_color: Color.InputType = 170,
        text_size: Int.InputType = 100,
        text_font: Font.InputType = None,
        hover_color: Color.InputType = 170,
    ) -> None:
        super().__init__()
        self.color = color
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.text_font = text_font
        self.hover_color = hover_color

    def _start(self) -> None:

        tmp = self.text_font(self.text_size).render(self.text, 0, self.color)
        self.width = tmp.get_width() * 1.3
        self.height = tmp.get_height() * 1.3

        hover_color = Color.adapt(self.hover_color)

        self.hover_animation = HoverAnimation(
            (self, "color", Color, self.color, Color.adapt(70)),
            (self, "width", Int, self.width, self.width + 3),
            (self, "height", Int, self.height, self.height + 3),
            (self, "text_color", Color, self.text_color, hover_color),
            duration=100,
        )
        self.click_animation = HoverAnimation(
            (self, "color", Color, self.color, Color.adapt(50)),
            (self, "width", Int, self.width, self.width - 3),
            (self, "height", Int, self.height, self.height - 3),
            (self, "text_color", Color, self.text_color, hover_color),
            duration=10,
        )

    def _build(self) -> None:
        text_surface = self.text_font(self.text_size).render(self.text, True, self.text_color)
        back = pg.Surface((self.width, self.height), pg.SRCALPHA)
        back.fill(self.color)
        back.blit(
            text_surface,
            (
                int((self.width - text_surface.get_width()) / 2),
                int((self.height - text_surface.get_height()) / 2),
            ),
        )
        self.image = back

    def _update(self, delta_time: int) -> None:
        self.hover_animation.play(delta_time, self.rect.collidepoint(*pg.mouse.get_pos()))
        if self.is_clicked:
            self.click_animation.play(delta_time, self.is_clicked)
