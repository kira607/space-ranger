import typing as t

import numpy as np
import pygame as pg

from space_ranger.common.color import GREEN, RED
from space_ranger.core import GameObject, Scene
from space_ranger.core.animation import Animation, ForwardBackAnimation
from space_ranger.core.component import Rectangle, Text
from space_ranger.core.scene import SceneId


class ExampleGameObj(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.example_component = self.add_component(Rectangle(200, 100, 100))
        self.transform.x = 50
        self.transform.y = 50


def color_to_array(color):
    return np.array((color.r, color.g, color.b, color.a))


def array_to_color(array):
    r = int(pg.math.clamp(array[0].item(), 0, 255))
    g = int(pg.math.clamp(array[1].item(), 0, 255))
    b = int(pg.math.clamp(array[2].item(), 0, 255))
    a = int(pg.math.clamp(array[3].item(), 0, 255))
    return pg.Color(r, g, b, a)


class Button(GameObject):

    def __init__(self, text: str = "Button") -> None:
        super().__init__()
        self.idle_color = pg.Color(127, 255, 127)
        self.idle_width = 100
        self.idle_height = 100
        self.font = None
        self.text = self.add_component(Text(text, self.font, 30, 127), 1)
        self.back = self.add_component(Rectangle(self.idle_color, self.text.width * 1.2, self.text.height * 1.3))
        self.transform.x = 100
        self.transform.y = 150
        self.transform.r = 200
        self.hover_animation = ForwardBackAnimation(
            self.idle_color,
            pg.Color(0, 0, 0, 255),
            duration=200,
            to_array=color_to_array,
            from_array=array_to_color,
        )

    def update(self, delta_time: int) -> None:
        pos = pg.mouse.get_pos()
        self.back.color = self.hover_animation.play(delta_time, self.back.rect.collidepoint(*pos))

class Playground(Scene):
    """A main menu state."""

    def __init__(self, scene_id: SceneId) -> None:
        super().__init__(scene_id)
        self.example_game_obj = self.add_game_object(ExampleGameObj())
        self.another_obj = self.add_game_object(Button("fgsdfgsdfgs"))
        self.another_obj.text.string = "Button"

    def draw(self, screen: pg.Surface) -> None:
        """Draw main menu on a given screen.

        :param pg.Surface screen: Target screen.
        """
        screen.fill(pg.Color(230, 230, 230, 200))
        super().draw(screen)
