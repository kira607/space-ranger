from __future__ import annotations

import typing as t

import pygame as pg

from .common import Collector, Observer
from .property import Angle, Color, Float, Font, Int, Property, String

if t.TYPE_CHECKING:
    from .game_object import GameObject

__all__ = [
    "Transform",
    "Rectangle",
]


def isdrawable(obj: object) -> bool:
    return hasattr(obj, "__drawable__") and obj.__drawable__


class Drawable(pg.sprite.Sprite):
    __drawable__ = True


class Component(Observer, Collector):
    """Game object component base class."""

    game_object: GameObject | None = None

    def accept_notification(self) -> None:
        """Accept a notification from property."""
        if self.game_object:
            self.game_object.accept_notification()


class SpriteComponent(Component, Drawable):
    def accept_notification(self) -> None:
        self.build()
        super().accept_notification()

    def build(self) -> None:
        pass


class Transform(Component):
    """Game object transform."""

    x = Float()
    y = Float()
    r = Angle()

    def __init__(self, x: float = 0, y: float = 0, r: float = 0) -> None:
        self.x = x
        self.y = y
        self.r = r

    @classmethod
    def from_vector(cls, vector: pg.Vector3) -> Transform:
        """Create a new Transform from `pygame.Vector3`."""
        return cls(vector.x, vector.y, vector.z)

    @property
    def vector(self) -> pg.Vector3:
        """Get transform as a vector."""
        return pg.Vector3(self.x, self.y, self.r)

    def __add__(self, other: Transform) -> Transform:
        """Add two trasform objects."""
        return Transform.from_vector(self.vector + other.vector)


class Rectangle(SpriteComponent):
    """Rectangle sprite."""

    color = Color()
    width = Int()
    height = Int()

    def __init__(self, color: pg.Color, width: int, height: int) -> None:
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.build()

    def build(self) -> None:
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()


class Text(SpriteComponent):
    """Text component."""

    string = String()
    font = Font()
    size = Int()
    color = Color()

    def __init__(
        self,
        string: String.input_type,
        font: Font.input_type,
        size: Int.input_type,
        color: Color.input_type,
    ) -> None:
        super().__init__()
        self.string = string
        self.font = font
        self.size = size
        self.color = color
        self.build()

    @property
    def width(self) -> int:
        return self.image.get_width()

    @property
    def height(self) -> int:
        return self.image.get_height()

    def build(self) -> None:
        self.image = self.font(self.size).render(self.string, False, self.color)
        self.rect = self.image.get_rect()
