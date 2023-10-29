from __future__ import annotations

from dataclasses import dataclass
from math import atan2, pi

import pygame as pg

from space_ranger.core import Scene, ctx
from space_ranger.core.asset.image_asset import ImageAsset
from space_ranger.core.utils import draw_arrow, get_text_surface


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


class Sprite(pg.sprite.Sprite):
    """A base sprite."""

    position: pg.math.Vector2
    rotation: float

    def __new__(cls, *args, **kwargs) -> None:  # noqa: D102
        obj = super().__new__(cls)
        obj.position = pg.math.Vector2()
        obj.rotation = 0.0
        obj.image = None
        obj.rect = None
        return obj

    def __init__(self) -> None:
        super().__init__()
        self.image = self._get_image()
        self._update_image()

    def _update_image(self) -> None:
        """Build a thing."""
        self.image = pg.transform.rotate(self._get_image(), -self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def _get_image(self) -> pg.Surface:
        raise NotImplementedError()

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


@dataclass
class SpaceshipCore:
    """Spaceship core."""

    power: float
    max_speed: float
    acceleration: float

    back_engine_power: float = 0
    front_engine_power: float = 0
    left_engine_power: float = 0
    right_engine_power: float = 0


class Spaceship(Sprite):
    """A player."""

    def __init__(self) -> None:
        self._original_image = pg.transform.scale(ImageAsset("spaceship.png").load().convert_alpha(), (100, 100))

        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)

        self.engine = SpaceshipCore(50, 10, 10)
        self.mass = 200
        self.density = 10
        super().__init__()

    @property
    def speed(self) -> float:
        """Get current spaceship speed."""
        return self.velocity.magnitude()

    @property
    def max_speed(self) -> float:
        """Get maximum spaceship speed."""
        return self.engine.max_speed

    def update(self, delta_time: int) -> None:
        """Update player."""
        self._update_engine()
        self._update_rotation()
        self._move()
        self._update_image()

    def _get_image(self) -> None:
        return self._original_image

    def _update_engine(self) -> None:
        keys = pg.key.get_pressed()
        self.engine.back_engine_power = float(keys[ctx.controls.move_forward])
        self.engine.front_engine_power = float(keys[ctx.controls.move_backward])
        self.engine.left_engine_power = float(keys[ctx.controls.move_right])
        self.engine.right_engine_power = float(keys[ctx.controls.move_left])

    def _update_rotation(self) -> None:
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        dx = mouse.x - ctx.screen.center.x
        dy = mouse.y - ctx.screen.center.y
        angle = atan2(dy, dx) * 180 / pi
        self.rotation = angle

    def _move(self) -> None:
        self.acceleration = self._calculate_acceleration()
        self.velocity += self.acceleration
        if self.velocity:
            self.velocity.clamp_magnitude_ip(self.engine.max_speed)
        self.position += self.velocity

    def _calculate_acceleration(self) -> pg.math.Vector2:
        acceleration = sum(self._get_forces(), start=pg.math.Vector2())
        if not acceleration:
            if not self.velocity:
                return acceleration
            acceleration = -self.velocity * self.engine.power * 0.3
        acceleration /= self.mass
        if acceleration.magnitude() <= 0.002:
            return pg.math.Vector2()
        return acceleration

    def _get_forces(self) -> list[pg.math.Vector2]:
        return [
            pg.math.Vector2(self.engine.back_engine_power * self.engine.power, 0).rotate(self.rotation),
            pg.math.Vector2(-self.engine.front_engine_power * self.engine.power * 0.6, 0).rotate(self.rotation),
            pg.math.Vector2(0, self.engine.left_engine_power * self.engine.power * 0.4).rotate(self.rotation),
            pg.math.Vector2(0, -self.engine.right_engine_power * self.engine.power * 0.4).rotate(self.rotation),
        ]

    def _draw_debug(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "red", self.rect, width=1)
        for force in self._get_forces():
            draw_arrow(surface, self.rect.center, force, "green")
        draw_arrow(surface, self.rect.center, self.velocity * 20, "yellow")
        draw_arrow(surface, self.rect.center, self.acceleration * 20, "red")
        debug_surface = get_text_surface(
            f"pos: {self.position}",
            f"rot: {round(self.rotation, 2)}",
            f"vel: {self.velocity}",
            f"acc: {self.acceleration}",
            f"spd: {self.speed}",
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
        )
        pos = pg.math.Vector2(self.rect.topleft)
        pos.y -= debug_surface.get_height()
        surface.blit(debug_surface, (pos))


class RectSprite(Sprite):
    """Rect sprite."""

    def __init__(self) -> None:
        self.width = 200
        self.height = 300
        super().__init__()

    def _get_image(self) -> pg.Surface:
        image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        image.fill(pg.Color(234, 255, 34, 127))
        return image


class Playground(Scene):
    """A main menu state."""

    def _start(self) -> None:
        self.entities = []

        self.camera_free_look = False
        self.camera_offset = pg.math.Vector2()
        self.camera = Camera(pg.Color(50, 50, 50), ctx.screen.surface, 1 / 1.5, 1)

        self.player = Spaceship()
        self.camera.add(self.player)
        self.entities.append(self.player)

        self.rect = RectSprite()
        self.camera.add(self.rect)
        self.entities.append(self.rect)
        self.rect.position = (300, 300)

    def _process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.exit_application()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.exit_application()
        if event.type == pg.KEYUP and event.key == pg.K_i:
            self.camera_free_look = not self.camera_free_look

    def _update(self, delta_time: int) -> None:
        self.player.update(delta_time)

        key = pg.key.get_pressed()

        # debug camera controller
        if self.camera_free_look and ctx.config.debug:
            cam_speed = 7
            zoom_speed = 0.01
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
            offset = pg.math.Vector2(pg.mouse.get_pos())
            offset -= ctx.screen.center
            if offset:
                offset.normalize_ip()
            offset *= offset.magnitude() * 20
            self.camera.center_at(self.player.position + offset)
            self.camera.zoom = 1 + (1 - self.camera._min_zoom) * (self.player.speed / self.player.max_speed)
            # if self.player.acceleration:
            #     self.camera.zoom -= 0.01
            # else:
            #     self.camera.zoom += 0.01

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
        lines.append(
            f"    zoom [{self.camera._min_zoom}, {self.camera._max_zoom}]: {round(self.camera._zoom_scale, 3)}"
        )
        debug_surface = get_text_surface(
            *lines,
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
            alignment="right",
        )
        surface.blit(debug_surface, (ctx.screen.width - debug_surface.get_width(), 0))
