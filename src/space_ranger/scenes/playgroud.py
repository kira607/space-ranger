from __future__ import annotations

from math import atan2, pi

import pygame as pg

from space_ranger.core import Scene, ctx
from space_ranger.core.asset import ImageAsset


class Player(pg.sprite.Sprite):
    """A player."""

    def __init__(self) -> None:
        super().__init__()
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 5
        self.rotation = 0
        self._build()

    def _build(self) -> None:
        rect_center = self.rect.center if self.rect else (0, 0)
        self.image = pg.Surface((100, 100), pg.SRCALPHA)
        self.image.fill(pg.Color(0, 0, 0))
        self.image = pg.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = rect_center

    def _input(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def _rotate(self) -> None:
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        dx = mouse.x - ctx.screen.center.x
        dy = mouse.y - ctx.screen.center.y
        angle = atan2(dy, dx) * 180 / pi
        self.rotation = -angle

    def update(self, delta_time: int) -> None:
        self._input()

        self._rotate()
        self._build()
        self.rect.center += self.direction * self.speed


class Background:
    def __init__(self) -> None:
        self.back = ImageAsset("Parallax60.png").load()
        w, h = self.back.get_width(), self.back.get_height()
        tiles_x = (ctx.screen.width // self.back.get_width()) + 1
        tiles_y = (ctx.screen.height // self.back.get_height()) + 1
        self.positions = [(w * i, h * j) for i in range(tiles_x) for j in range(tiles_y)]

    def draw(self, screen) -> None:
        for p in self.positions:
            screen.blit(self.back, p)


class Playground(Scene):
    """A main menu state."""

    def _start(self) -> None:
        self.background = Background()
        self.player = Player()
        self.player_group = pg.sprite.GroupSingle(self.player)
        print(self.player.rect.center)
        print(ctx.screen.center)
        self.player.rect.center = ctx.screen.center
        print(self.player.rect.center)

    def _process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.exit_application()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.exit_application()

    def _update(self, delta_time: int) -> None:
        self.player_group.update(delta_time)

    def _draw(self, screen: pg.Surface) -> None:
        screen.fill((50, 50, 50))
        # self.background.draw(screen)
        self.player_group.draw(screen)
