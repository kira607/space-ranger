import pygame as pg

from space_ranger.core import Scene
from space_ranger.core.scene import SceneId
from space_ranger.prefabs import Button, Checkbox, Slider


class Playground(Scene):
    """A main menu state."""

    button = Button(hover_color=(127, 255, 127))
    checkbox = Checkbox()
    slider = Slider()

    def __init__(self, scene_id: SceneId) -> None:
        super().__init__(scene_id)

    def _start(self) -> None:
        offset = 50
        offset_left = 200
        self.background_color = pg.Color(230, 230, 230, 200)
        self.button.set_transform(offset_left, offset)
        self.checkbox.set_transform(offset_left, self.button.rect.bottom + offset)
        self.slider.set_transform(offset_left, self.checkbox.rect.bottom + offset)
