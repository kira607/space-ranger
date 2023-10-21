from dataclasses import dataclass

import pygame as pg

from ._component import Component


@dataclass(slots=True)
class Transform(Component):
    """A component describing a position of an entity in 2d space."""

    x: float = 0
    y: float = 0
    rotation: float = 0

    @property
    def position(self) -> pg.math.Vector2:
        """Get position as a 2d vector."""
        return pg.math.Vector2(self.x, self.y)

    @position.setter
    def position(self, value: pg.math.Vector2 | tuple[float, float]) -> None:
        """Set position from 2d vector."""
        self.x, self.y = value
