from __future__ import annotations

import typing as t

import pygame as pg

from ._ctx import ctx

if t.TYPE_CHECKING:
    from .scene import Scene


class Camera(pg.sprite.LayeredUpdates):
    """A scene camera."""

    _MIN_ZOOM = 1
    _MAX_ZOOM = 1

    def __init__(self, scene: Scene, screen: pg.Surface = None) -> None:
        super().__init__()
        self._scene: Scene = scene
        self._offset: pg.math.Vector2 = pg.math.Vector2()
        self._zoom_scale: float = 1

        self._screen: pg.Surface
        self._center_offset: pg.math.Vector2
        self._camera_scale: pg.math.Vector2
        self._camera_surface: pg.Sufrace
        self._camera_rect: pg.Rect
        self._zoom_offset: pg.math.Vector2

        if screen:
            self._use_screen(screen)

    @property
    def zoom(self) -> float:
        """Get zoom value."""
        return min(self._zoom_scale, self._MAX_ZOOM)

    @zoom.setter
    def zoom(self, value: float) -> None:
        """Set zoom value.

        Zoom value equaling 1 is a default zoom.

        :param value: New zoom value.
        :type value: float
        """
        self._zoom_scale = max(value, self._MIN_ZOOM)

    def setup_zoom(self, min_zoom: float = 1, max_zoom: float = 1) -> None:
        self._MIN_ZOOM = float(min_zoom)
        self._MAX_ZOOM = float(max_zoom)

    def center_at(self, pos: pg.math.Vector2) -> None:
        """Center camera at given point.

        :param pos: Center point to focus on.
        :type pos: pg.math.Vector2
        """
        self._offset = pos - self._center_offset
        for sprite in self.sprites():
            sprite.rect.topleft = sprite.rect.topleft - self._offset + self._zoom_offset

    def custom_draw(self, screen: pg.Surface) -> None:
        """Draw sprites."""
        self._use_screen(screen)
        self._camera_surface.fill(self._scene.background_color)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.layer):
            self._camera_surface.blit(sprite.image, sprite.rect)
            if ctx.config.debug:
                pg.draw.rect(self._camera_surface, (255, 0, 0), sprite.rect, 1)

        scaled_surface = pg.transform.scale(self._camera_surface, self._camera_scale * self._zoom_scale)
        scaled_rect = scaled_surface.get_rect(center=self._center_offset)

        self._screen.blit(scaled_surface, scaled_rect)
        if ctx.config.debug:
            pg.draw.rect(self._screen, (255, 255, 0), scaled_rect, 1)

    def _use_screen(self, screen: pg.Surface) -> None:
        self._screen = screen
        self._center_offset = pg.math.Vector2(
            self._screen.get_size()[0] // 2,
            self._screen.get_size()[1] // 2,
        )
        self._camera_scale = pg.Vector2(self._screen.get_rect().size) / self._MIN_ZOOM
        self._camera_surface = pg.Surface(self._camera_scale, pg.SRCALPHA)
        self._camera_rect = self._camera_surface.get_rect(center=self._center_offset)
        self._zoom_offset = pg.math.Vector2(self._camera_scale // 2 - self._center_offset)
