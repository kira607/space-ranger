import pygame as pg

from space_ranger.core import Animation, GameObject
from space_ranger.property import Position


class UIElement(GameObject):
    """A base UI element."""

    position = Position()

    def __init__(self, position: pg.Vector2 | None = None) -> None:
        self._animations: list[Animation] = []
        if position is not None:
            self.position.set_value(position)
