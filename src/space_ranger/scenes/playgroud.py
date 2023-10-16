from __future__ import annotations

from math import atan2, pi

import pygame as pg

from space_ranger.core import Scene, ctx
from space_ranger.core.utils import get_text_surface


class Camera:
    """A scene camera."""

    def __init__(
        self,
        background_color: pg.Color,
        screen: pg.Surface,
        min_zoom: float = 1,
        max_zoom: float = 1,
    ) -> None:
        self._sprites: list[pg.sprite.Sprite] = []
        self._background_color = background_color

        self._min_zoom = round(float(min_zoom), 3)
        self._max_zoom = round(float(max_zoom), 3)
        self._zoom_scale: float = 1

        self._offset: pg.math.Vector2 = pg.math.Vector2()
        self._position: pg.math.Vector2 = pg.math.Vector2()

        self._screen = screen
        self._vscreen_size = pg.Vector2(self._screen.get_rect().size) / self._min_zoom
        self._vscreen_surface = pg.Surface(self._vscreen_size, pg.SRCALPHA)
        self._vscreen_center = pg.math.Vector2(
            self._vscreen_surface.get_size()[0] // 2,
            self._vscreen_surface.get_size()[1] // 2,
        )
        self._vscreen_rect = self._vscreen_surface.get_rect(center=self._vscreen_center)

        self._calculate_offset()

    def add(self, sprite: pg.sprite.Sprite) -> None:
        """Add a sprite."""
        self._sprites.append(sprite)

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

    def center_at(self, pos: pg.math.Vector2) -> None:
        """Center camera at given point.

        :param pos: Center point to focus on.
        :type pos: pg.math.Vector2
        """
        self._position = pos
        self._calculate_offset()

    def draw(self) -> None:
        """Draw sprites."""
        self._vscreen_surface.fill(self._background_color)
        for sprite in self._sprites:
            sprite.rect.center = sprite.position + self._offset
            self._vscreen_surface.blit(sprite.image, sprite.rect.topleft)
            if ctx.config.debug:
                sprite._draw_debug(self._vscreen_surface)
            # sprite.draw(self._vscreen_surface)

        scaled_surface = pg.transform.scale(self._vscreen_surface, self._vscreen_size * self.zoom)
        scaled_rect = scaled_surface.get_rect(center=self._screen.get_rect().center)
        self._screen.blit(scaled_surface, scaled_rect)
        if ctx.config.debug:
            pg.draw.rect(self._screen, (255, 255, 0), scaled_rect, 1)

    def _clamp_zoom(self, zoom_value: float) -> float:
        return pg.math.clamp(zoom_value, self._min_zoom, self._max_zoom)

    def _calculate_offset(self) -> None:
        zoom_offset = pg.math.Vector2(self._vscreen_size // 2 - self._vscreen_center)
        self._offset = -self._position + self._vscreen_center + zoom_offset


class Thing(pg.sprite.Sprite):
    """A base thing."""

    def __init__(self) -> None:
        super().__init__()
        self.position = pg.math.Vector2(0, 0)
        self.rotation = 0
        self.image = None
        self.rect = None
        self.build()

    def build(self) -> None:
        self._build_image()
        self.image = pg.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def _build_image(self) -> None:
        raise NotImplementedError()


class Player(Thing):
    """A player."""

    def __init__(self) -> None:
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 5
        super().__init__()

    @property
    def is_moving(self) -> bool:
        """Check if the player is moving."""
        return self.direction != pg.math.Vector2()

    def _build_image(self) -> None:
        self.image = pg.Surface((100, 100), pg.SRCALPHA)
        self.image.fill(pg.Color(0, 0, 0))

    def _input(self) -> None:
        keys = pg.key.get_pressed()

        if keys[ctx.controls.move_up]:
            self.direction.y = -1
        elif keys[ctx.controls.move_down]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[ctx.controls.move_right]:
            self.direction.x = 1
        elif keys[ctx.controls.move_left]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.is_moving:
            self.direction.normalize_ip()

    def _rotate(self) -> None:
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        dx = mouse.x - ctx.screen.center.x
        dy = mouse.y - ctx.screen.center.y
        angle = atan2(dy, dx) * 180 / pi
        self.rotation = -angle

    def update(self, delta_time: int) -> None:
        self._input()
        self.position += self.direction * self.speed
        self._rotate()
        self.build()

    def _draw_debug(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "red", self.rect, width=1)
        debug_surface = get_text_surface(
            f"pos: {self.position}",
            f"rot: {round(self.rotation, 2)}",
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
        )
        pos = pg.math.Vector2(self.rect.topleft)
        pos.y -= debug_surface.get_height()
        surface.blit(debug_surface, (pos))


class RectSprite(Thing):

    def __init__(self) -> None:
        self.width = 200
        self.height = 300
        super().__init__()

    def _build_image(self) -> None:
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.image.fill(pg.Color(234, 255, 34, 127))

    def _draw_debug(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "red", self.rect, width=1)
        debug_surface = get_text_surface(
            f"pos: {self.position}",
            f"rot: {round(self.rotation, 2)}",
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
        )
        pos = pg.math.Vector2(self.rect.topleft)
        pos.y -= debug_surface.get_height()
        surface.blit(debug_surface, (pos))


class Playground(Scene):
    """A main menu state."""

    def _start(self) -> None:
        self.entities = []
        self.camera = Camera(pg.Color(50, 50, 50), ctx.screen.surface, 1 / 1.5, 1)

        self.player = Player()
        self.camera.add(self.player)
        self.entities.append(self.player)

        self.rect = RectSprite()
        self.camera.add(self.rect)
        self.entities.append(self.rect)

        # self.camera.center_at(pg.math.Vector2(0, 0))

    def _process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.exit_application()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.exit_application()

    def _update(self, delta_time: int) -> None:
        self.player.update(delta_time)
        if ctx.config.debug:
            # debug camera controller
            cam_speed = 7
            zoom_speed = 0.01
            key = pg.key.get_pressed()
            if key[pg.K_p]:
                self.camera.center_at(self.camera._position + (0, -cam_speed))
            if key[pg.K_SEMICOLON]:
                self.camera.center_at(self.camera._position + (0, cam_speed))
            if key[pg.K_l]:
                self.camera.center_at(self.camera._position + (-cam_speed, 0))
            if key[pg.K_QUOTE]:
                self.camera.center_at(self.camera._position + (cam_speed, 0))
            if key[pg.K_o]:
                self.camera.zoom -= zoom_speed
            if key[pg.K_LEFTBRACKET]:
                self.camera.zoom += zoom_speed
        else:
            self.camera.center_at(self.player.position)
            if self.player.is_moving:
                self.camera.zoom -= 0.01
            else:
                self.camera.zoom += 0.01

    def _draw(self, screen: pg.Surface) -> None:
        # screen.fill((50, 50, 50))
        self.camera.draw()
        if ctx.config.debug:
            self._draw_debug(screen)

    def _draw_debug(self, surface: pg.Surface) -> None:
        lines = []
        for entity in self.entities:
            lines.append(f"Entity: {entity.__class__.__name__}:")
            lines.append(f"    position: {entity.position}")
            lines.append(f"    rect: {entity.rect}")
            lines.append("------------------")
        lines.append("Camera:")
        lines.append(f"    pos: {self.camera._position}")
        lines.append(f"    rect: {self.camera._vscreen_rect}")
        lines.append(f"    center: {self.camera._vscreen_center}")
        lines.append(f"    size: {self.camera._vscreen_size}")
        lines.append(f"    offset: {self.camera._offset}")
        lines.append(f"    zoom [{self.camera._min_zoom}, {self.camera._max_zoom}]: {round(self.camera._zoom_scale, 3)}")
        debug_surface = get_text_surface(
            *lines,
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
            alignment="right",
        )
        surface.blit(debug_surface, (ctx.screen.width - debug_surface.get_width(), 0))
