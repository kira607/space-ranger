from dataclasses import dataclass, field

import pygame as pg

from ._component import Component


@dataclass(slots=True)
class PhysicsBody(Component):
    """A component describing entity movement physics."""

    mass: float = 1
    constant_forces: list[pg.math.Vector2] = field(default_factory=list)
    forces: list[pg.math.Vector2] = field(default_factory=list)
    velocity: pg.math.Vector2 = field(default_factory=pg.math.Vector2)
    acceleration: pg.math.Vector2 = field(default_factory=pg.math.Vector2)
