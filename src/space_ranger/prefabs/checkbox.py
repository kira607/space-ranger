import pygame as pg

from space_ranger.core import GameObject
from space_ranger.core.animation import HoverAnimation
from space_ranger.core.property import Bool, Color, Int


class Checkbox(GameObject):
    """Checkbox."""

    is_checked = Bool(False)
    back_color = Color(170)
    size = Int(50)

    def __init__(self) -> None:
        super().__init__()
        self.hover_animation = HoverAnimation(
            (self, "back_color", Color, self.back_color, Color.adapt(70)),
            (self, "size", Int, self.size, self.size + 1),
            duration=100,
        )
        self.click_animation = HoverAnimation(
            (self, "back_color", Color, self.back_color, Color.adapt(50)),
            (self, "size", Int, self.size, self.size - 1),
            duration=10,
        )
        self._checked_on_previous_frame = False

    def _build(self) -> None:
        root = pg.Surface((self.size, self.size), pg.SRCALPHA)
        root.fill(self.back_color)
        if self.is_checked:
            check_mark = pg.Surface((self.size * 0.7, self.size * 0.7), pg.SRCALPHA)
            check_mark.fill(Color.adapt(255))
            root.blit(check_mark, (self.size * 0.15, self.size * 0.15))
        self.image = root

    def _update(self, delta_time: int) -> None:
        self.hover_animation.play(delta_time, self.is_hovered)
        if self.is_clicked:
            self.click_animation.play(delta_time, self.is_clicked)
            if not self._checked_on_previous_frame:
                self.is_checked = not self.is_checked
                self._checked_on_previous_frame = True
        else:
            self._checked_on_previous_frame = False
