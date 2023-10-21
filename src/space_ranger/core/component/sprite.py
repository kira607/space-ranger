from dataclasses import dataclass, field

import pygame as pg

from ._component import Component


@dataclass(slots=True)
class Sprite(Component, pg.sprite.DirtySprite):
    """2D sprite component."""

    source: pg.Surface = field(default=None)
    image: pg.Surface = field(default=None)
    rect: pg.Rect = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        if self.image is None:
            self.image = self.source
        if self.rect is None:
            self.rect = self.image.get_rect()
