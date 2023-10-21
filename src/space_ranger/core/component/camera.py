from dataclasses import dataclass, field

import pygame as pg

from space_ranger.core import ctx

from ._component import Component


@dataclass(slots=True)
class Camera(Component):
    """Camera component."""

    screen: pg.Surface = field(default=None)
    min_zoom: float = 1
    max_zoom: float = 1
    offset: pg.math.Vector2 = field(default_factory=pg.math.Vector2)
    vscreen_size: pg.math.Vector2 = field(default=pg.math.Vector2)
    vscreen_surface: pg.Surface = field(default=None)
    vscreen_center: pg.math.Vector2 = field(default=pg.math.Vector2)
    vscreen_rect: pg.Rect = field(default=None)
    background_color: pg.color.Color = field(default_factory=lambda: pg.color.Color("gray12"))
    _zoom_scale: float = 1

    def __post_init__(self) -> None:  # noqa: D105
        self.screen = ctx.screen.surface
        self.offset = pg.math.Vector2()
        self.vscreen_size = pg.Vector2(self.screen.get_rect().size) / self.min_zoom
        self.vscreen_surface = pg.Surface(self.vscreen_size, pg.SRCALPHA)
        self.vscreen_center = pg.math.Vector2(
            self.vscreen_surface.get_size()[0] // 2,
            self.vscreen_surface.get_size()[1] // 2,
        )
        self.vscreen_rect = self.vscreen_surface.get_rect(center=self.vscreen_center)

    @property
    def zoom(self) -> float:
        """Get zoom value."""
        return self._clamp_zoom(self._zoom_scale)

    @zoom.setter
    def zoom(self, value: float) -> None:
        """Set zoom value.

        Zoom value equaling 1 is a default zoom.

        :param value: New zoom value.
        :type value: float
        """
        self._zoom_scale = self._clamp_zoom(value)

    def _clamp_zoom(self, zoom_value: float) -> float:
        return pg.math.clamp(zoom_value, self.min_zoom, self.max_zoom)
