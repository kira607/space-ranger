import typing as t

import pygame as pg

from space_ranger.common.color import GREEN, RED
from space_ranger.core import Scene
from space_ranger.ui import Button, Text


class ButtonBack(GameObject):
    sprite = Sprite(Sprite.RECT)


class ButtonText(GameObject):
    text = Text("Button")


class Button(GameObject):
    back = ButtonBack()
    text = ButtonText("Button")


class Playground(Scene):
    """A main menu state."""

    button = Button(pg.Vector2(200, 200), text="Button", text_color=RED, color=GREEN)
    my_text = Text(pg.Vector2(100, 100), size=250)

    def process_event(self, event: pg.event.Event) -> None:
        """Process pygame event.

        :param pg.event.Event event: A pygame event to process.
        """
        # if self.text._img.get_rect().collidepoint(pg.mouse.get_pos()):
        #     self.text.on_hover()

    def draw(self, screen: pg.Surface) -> None:
        """Draw main menu on a given screen.

        :param pg.Surface screen: Target screen.
        """
        screen.fill(pg.Color(230, 230, 230, 200))
        super().draw(screen)
