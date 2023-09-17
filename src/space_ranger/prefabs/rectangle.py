import pygame as pg

from space_ranger.core import GameObject
from space_ranger.core.property import Color, Int


class Rectangle(GameObject):
    """Rectangle."""

    color = Color(127)
    width = Int(100)
    height = Int(100)

    def _build(self) -> None:
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.image.fill(self.color)
