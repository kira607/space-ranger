import pygame as pg

from space_ranger.core import GameObject
from space_ranger.core.animation import HoverAnimation
from space_ranger.core.property import Color, Float, Int


class Slider(GameObject):
    """Slider UI."""

    value = Float(0, 0, 1)
    height = Int(50)
    width = Int(300)
    back_color = Color(170)
    slider_color = Color(255)

    def __init__(self) -> None:
        super().__init__()
        self.hover_animation = HoverAnimation(
            (self, "back_color", Color, self.back_color, Color.adapt(70)),
            duration=200,
        )

    def _build(self) -> None:
        root = pg.Surface((self.width, self.height), pg.SRCALPHA)
        root.fill(self.back_color)

        slider = pg.Surface((self.height, self.height), pg.SRCALPHA)
        slider.fill(self.slider_color)

        root.blit(
            slider,
            (
                (self.width - self.height) * self.value,
                0,
            ),
        )
        self.image = root

    def _update(self, delta_time: int) -> None:
        self.hover_animation.play(delta_time, self.is_hovered)

        if self.is_clicked:
            self.value = pg.math.clamp(
                (pg.mouse.get_pos()[0] - self.rect.x - self.height / 2) / (self.width - self.height),
                0,
                1,
            )
