from __future__ import annotations

import random
from dataclasses import InitVar, dataclass, field
from math import atan2, pi

import pygame as pg

from space_ranger.core import Scene, ctx
from space_ranger.core.asset.image_asset import ImageAsset
from space_ranger.core.component import Camera, Script, Sprite, Transform
from space_ranger.core.entity import Entity, make_entity
from space_ranger.core.system import DebugSystem, RenderingSystem, ScriptingSystem, SpriteRotationSystem, System
from space_ranger.core.utils import draw_arrow, get_text_surface, rect


class Thing(pg.sprite.Sprite):
    """A base thing."""

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


@dataclass(slots=True)
class Engine:
    """A spaceship engine."""

    power: float = 0
    state: bool = False

    def __bool__(self) -> bool:
        """Get a boolean value of an engine.

        :return: True if it is ignited, False otherwise.
        :rtype: bool
        """
        return self.state

    @property
    def value(self) -> float:
        """Get engine power value.

        :return: Engine power if it is ignited, 0 otherwise.
        :rtype: float
        """
        return self.power * self.state


@dataclass(slots=True)
class SpaceshipReactor:
    """A spaceship reactor.

    Produces a power for all spaceship engines
    including a stabalizer engine.
    """

    power: InitVar[float]
    back_engine: Engine = field(default_factory=Engine)
    front_engine: Engine = field(default_factory=Engine)
    left_engine: Engine = field(default_factory=Engine)
    right_engine: Engine = field(default_factory=Engine)
    stabalizer_engine: Engine = field(default_factory=Engine)

    def __post_init__(self, power: float) -> None:
        """Post init reactor."""
        self.back_engine.power = power
        self.front_engine.power = power * 0.6
        self.left_engine.power = power * 0.4
        self.right_engine.power = power * 0.4
        self.stabalizer_engine.power = power * 0.8

    def get_acceleration_vector(self, velocity: pg.math.Vector2, mass: float) -> pg.math.Vector2:
        """Get a vector describing a spaceship acceleration.

        Acceleration is a vector that is a sum of all engines
        forces applied to a spaceship.
        """
        v = pg.math.Vector2(
            self.back_engine.value - self.front_engine.value,
            self.left_engine.value - self.right_engine.value,
        )
        v += self.get_stabilization_vector(velocity, mass)
        return v

    def get_stabilization_vector(self, velocity: pg.math.Vector2, mass: float) -> pg.math.Vector2:
        """Get a stabilization force vector.

        A stabalizer engine prevents a spaceship from infinite floating
        in space. Stabalizer simulates air conditions, like if a spaceship
        were in air and there were air force.

        Stabalizer force vector should be applied to a spaceship velocity,
        not acceleration.

        :param velocity: Current spaceship velocity.
        :type velocity: pg.math.Vector2
        :param mass: A spaceship total mass.
        :type mass: float

        :return: Stabalizer force vector.
        :rtype: pg.math.Vector2
        """
        v = velocity.magnitude()
        ro = 1.4
        S = 100
        A = 0.3
        k = ro * S * A * v * v
        return -velocity * k
        stabalizer_force_vector = -(velocity * mass) / (self.stabalizer_engine.power)
        return stabalizer_force_vector


class Spaceship(Thing):
    """A player."""

    def __init__(self) -> None:
        # physics vectors
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.velocity_stabilizer = pg.math.Vector2(0, 0)

        # ship parts
        self.reactor = SpaceshipReactor(500)
        self.mass = self.physics.mass
        self._max_speed = self._estimate_max_speed()

        self._original_image = pg.transform.scale(ImageAsset("spaceship.png").load().convert_alpha(), (100, 100))

        super().__init__()

    @property
    def speed(self) -> float:
        """Get current spaceship speed."""
        return self.velocity.magnitude()

    @property
    def max_speed(self) -> float:
        """Get maximum spaceship speed."""
        return self._max_speed

    def update(self, delta_time: int) -> None:
        """Update player."""
        self._input()
        self._update_rotation()
        self._apply_forces()
        self._move(delta_time / 1000)
        self._update_image()

    def _get_image(self) -> None:
        return self._original_image

    def _input(self) -> None:
        keys = pg.key.get_pressed()
        self.reactor.back_engine.state = keys[ctx.controls.move_forward]
        self.reactor.front_engine.state = keys[ctx.controls.move_backward]
        self.reactor.left_engine.state = keys[ctx.controls.move_right]
        self.reactor.right_engine.state = keys[ctx.controls.move_left]

    def _update_rotation(self) -> None:
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        dx = mouse.x - ctx.screen.center.x
        dy = mouse.y - ctx.screen.center.y
        angle = atan2(dy, dx) * 180 / pi
        self.rotation = angle

    def _apply_forces(self) -> None:
        self.physics.forces = [self.reactor.get_acceleration_vector(self.velocity, self.mass)]

    def _move(self, delta_time: float) -> None:
        self.acceleration = self.reactor.get_acceleration_vector(self.velocity, self.mass)
        self.velocity_stabilizer = self.reactor.get_stabilization_vector(self.velocity, self.mass)
        self.acceleration.rotate_ip(self.rotation)
        self.acceleration /= self.mass
        self.velocity = self.velocity + self.acceleration * delta_time
        self.position = self.position + self.velocity * delta_time

    def _estimate_max_speed(self) -> float:
        v = 0
        max_speed = 0
        for _ in range(1000):  # more cycles = more presiciton
            a = self.reactor.back_engine.power / self.mass
            v += a
            v += self.reactor.get_stabilization_vector(pg.math.Vector2(v, 0), self.mass).magnitude()
        max_speed = v
        return 1

    def _draw_debug(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "red", self.rect, width=1)
        vector_scaling_coeff = 100
        draw_arrow(surface, self.rect.center, self.velocity * vector_scaling_coeff, "yellow", 3)
        draw_arrow(surface, self.rect.center, self.acceleration * vector_scaling_coeff, "red", 3)
        draw_arrow(surface, self.rect.center, self.velocity_stabilizer * vector_scaling_coeff, "green", 3)
        debug_surface = get_text_surface(
            f"pos: {self.position}",
            f"rot: {round(self.rotation, 2)}",
            f"vel: {self.velocity}",
            f"acc: {self.acceleration}",
            f"spd: {self.speed}",
            f"mxs: {self.max_speed}",
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
        )
        pos = pg.math.Vector2(self.rect.topleft)
        pos.y -= debug_surface.get_height()
        surface.blit(debug_surface, (pos))


@dataclass(slots=True)
class EscHandler(Script):
    """Ecs key handler."""

    def _update(self, events: list[pg.event.Event], delta_time: int) -> None:
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.scene.exit_application()


@dataclass(slots=True)
class PlayerController(Script):
    """Simple player controller."""

    speed: int = 5
    camera: Entity = field(default=None)

    def _update(self, events: list[pg.event.Event], delta_time: int) -> None:
        self._update_rotation()
        keys = pg.key.get_pressed()
        pos = self.entity.transform
        if keys[ctx.controls.move_forward]:
            pos.y -= self.speed
        if keys[ctx.controls.move_backward]:
            pos.y += self.speed
        if keys[ctx.controls.move_right]:
            pos.x += self.speed
        if keys[ctx.controls.move_left]:
            pos.x -= self.speed

        self.camera.transform.position = pos.position

    def _update_rotation(self) -> None:
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        dx = mouse.x - ctx.screen.center.x
        dy = mouse.y - ctx.screen.center.y
        angle = atan2(dy, dx) * 180 / pi
        self.entity.transform.rotation = angle


@dataclass(slots=True)
class CameraSetup(Script):
    """Camera setup script."""

    def _start(self) -> None:
        cam: Camera = self.entity.get_component(Camera)
        cam.background_color = pg.Color(50, 50, 50)


@dataclass(slots=True)
class InstantiateTest(Script):
    """Object instantiation test."""

    spawn_rate: int = 10
    elapsed: int = 0
    current_rects: int = 0
    max_rects: int = 1000

    def _update(self, events: list[pg.event.Event], delta_time: int) -> None:
        self.elapsed += delta_time
        if self.elapsed >= self.spawn_rate:
            if self.current_rects >= self.max_rects:
                return
            self._spawn_rect()
            self.current_rects = self.current_rects + 1

    def _spawn_rect(self) -> None:
        x = random.randint(-ctx.screen.width // 2, ctx.screen.width // 2)
        y = random.randint(-ctx.screen.height // 2, ctx.screen.height // 2)
        rotation = random.randint(0, 360)
        size = random.randint(10, 50)
        color = pg.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 127)
        entity = make_entity(
            Transform(x=x, y=y, rotation=rotation),
            Sprite(source=rect(size, size, color)),
        )
        self.scene.instantiate(entity)


class Playground(Scene):
    """A main menu state."""

    def _get_entities(self) -> set[Entity]:
        camera = make_entity(
            Camera(),
            CameraSetup(),
        )

        return {
            # camera
            camera,
            # rect
            make_entity(
                Transform(x=300, y=300),
                Sprite(source=rect(200, 300, pg.Color(234, 255, 34, 127))),
            ),
            # player
            make_entity(
                Sprite(source=pg.transform.scale(ImageAsset("spaceship.png").load().convert_alpha(), (100, 100))),
                PlayerController(camera=camera),
            ),
            make_entity(EscHandler()),
            # make_entity(InstantiateTest()),
        }

    def _get_systems(self) -> set[System]:
        return {
            ScriptingSystem(group=0),
            SpriteRotationSystem(group=1),
            RenderingSystem(group=2),
            # DebugSystem(group=3),
        }

    # def _start(self) -> None:
    #     self.entities = []

    #     self.camera_free_look = False
    #     self.camera_offset = pg.math.Vector2()
    #     self.camera = Camera(pg.Color(50, 50, 50), ctx.screen.surface, 1 / 1.5, 1)

    #     self.player = Spaceship()
    #     self.camera.add(self.player)
    #     self.entities.append(self.player)

    #     self.rect = RectSprite()
    #     self.camera.add(self.rect)
    #     self.entities.append(self.rect)
    #     self.rect.position = (300, 300)

    # def _process_event(self, event: pg.event.Event) -> None:
    #     if event.type == pg.QUIT:
    #         self.exit_application()
    #     if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
    #         self.exit_application()

    # def _update(self, delta_time: int) -> None:
    #     self.player.update(delta_time)

    #     key = pg.key.get_pressed()

    #     if key[pg.K_i]:
    #         self.camera_free_look = not self.camera_free_look

    #     # debug camera controller
    #     if self.camera_free_look and ctx.config.debug:
    #         cam_speed = 7
    #         zoom_speed = 0.01
    #         if key[pg.K_p]:
    #             self.camera.center_at(self.camera._position + (0, -cam_speed))
    #         if key[pg.K_SEMICOLON]:
    #             self.camera.center_at(self.camera._position + (0, cam_speed))
    #         if key[pg.K_l]:
    #             self.camera.center_at(self.camera._position + (-cam_speed, 0))
    #         if key[pg.K_QUOTE]:
    #             self.camera.center_at(self.camera._position + (cam_speed, 0))
    #         if key[pg.K_o]:
    #             self.camera.zoom -= zoom_speed
    #         if key[pg.K_LEFTBRACKET]:
    #             self.camera.zoom += zoom_speed
    #     else:
    #         offset = pg.math.Vector2(pg.mouse.get_pos())
    #         offset -= ctx.screen.center
    #         if offset:
    #             offset.normalize_ip()
    #         offset *= offset.magnitude() * 20
    #         self.camera.center_at(self.player.position + offset)
    #         self.camera.zoom = 1 + (1 - self.camera._min_zoom) * (self.player.speed / self.player.max_speed)
    #         if self.player.acceleration:
    #             self.camera.zoom -= 0.01
    #         else:
    #             self.camera.zoom += 0.01

    # def _draw(self, screen: pg.Surface) -> None:
    #     # screen.fill((50, 50, 50))
    #     self.camera.draw()
    #     if ctx.config.debug:
    #         self._draw_debug(screen)

    # def _draw_debug(self, surface: pg.Surface) -> None:
    #     lines = []
    #     for entity in self.entities:
    #         lines.append(f"Entity: {entity.__class__.__name__}:")
    #         lines.append(f"    position: {entity.position}")
    #         lines.append(f"    rect: {entity.rect}")
    #         lines.append("------------------")
    #     lines.append("Camera:")
    #     lines.append(f"    pos: {self.camera._position}")
    #     lines.append(f"    rect: {self.camera._vscreen_rect}")
    #     lines.append(f"    center: {self.camera._vscreen_center}")
    #     lines.append(f"    size: {self.camera._vscreen_size}")
    #     lines.append(f"    offset: {self.camera._offset}")
    #     lines.append(
    #         f"    zoom [{self.camera._min_zoom}, {self.camera._max_zoom}]: {round(self.camera._zoom_scale, 3)}"
    #     )
    #     debug_surface = get_text_surface(
    #         *lines,
    #         font=ctx.debug_text_font,
    #         color=ctx.debug_text_color,
    #         background=ctx.debug_text_background,
    #         antialias=True,
    #         alignment="right",
    #     )
    #     surface.blit(debug_surface, (ctx.screen.width - debug_surface.get_width(), 0))
