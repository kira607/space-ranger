from __future__ import annotations

import typing as t

import pygame as pg

from space_ranger.core import ctx
from space_ranger.core.component import Camera, ComponentKey, Sprite
from space_ranger.core.entity import Entity

from ._system import System


if t.TYPE_CHECKING:
    from space_ranger.core.scene import Scene


class MissingCameraEntityError(Exception):
    """An error raised when a scene is missing an entity with camera component."""

    def __init__(self, scene: Scene) -> None:
        msg = (
            f"A '{scene.id}' scene missing an entity with camera component, "
            "required for RenderingSystem"
        )
        super().__init__(msg)


class TooManyCameraEntitiesError(Exception):
    """An error raised when a scene has too many entities with camera component."""

    def __init__(self, scene: Scene, count: int) -> None:
        msg = (
            f"A '{scene.id}' scene has too many entities with camera component, "
            f"expected to have 1, got {count}"
        )
        super().__init__(msg)


class RenderingSystem(System):
    """Rendering system."""

    def __init__(self, group: int = 0) -> None:
        super().__init__(group=group)
        self.camera_entity: Entity = None
        self.prev_transform = None
        self.prev_zoom = None

    @property
    def _camera_component(self) -> Camera:
        return self.camera_entity.get_component(Camera)

    def _match_entity(self, entity: Entity) -> set[ComponentKey]:
        required_components = {Sprite}
        if entity.match(*required_components):
            return required_components
        return set()

    def _calculate_offset(self) -> None:
        cam = self._camera_component
        zoom_offset = pg.math.Vector2(cam.vscreen_size // 2 - cam.vscreen_center)
        return -self.camera_entity.transform.position + cam.vscreen_center + zoom_offset


@RenderingSystem.before_start
def _before_start(self: RenderingSystem) -> None:
    # find camera entity in the scene
    matches = self.scene.find_entities(Camera)
    if not matches:
        raise MissingCameraEntityError(self.scene)
    if len(matches) > 1:
        raise TooManyCameraEntitiesError(self.scene, len(matches))
    self.camera_entity = matches.pop()


@RenderingSystem.before_update
def _before_update(self: RenderingSystem, events: list[pg.event.Event], delta_time: int) -> None:
    cam = self._camera_component
    cam.vscreen_surface.fill(cam.background_color)
    cam.offset = self._calculate_offset()


@RenderingSystem.update_entity
def _update_entity(self: RenderingSystem, entity_id: int, events: list[pg.event.Event], delta_time: int) -> None:
    sprite: Sprite = self.queued_entities[entity_id][Sprite]
    cam = self._camera_component
    sprite.rect.center = sprite.entity.transform.position + cam.offset
    cam.vscreen_surface.blit(sprite.image, sprite.rect.topleft)
    # if ctx.config.debug:
        # sprite._draw_debug(self._vscreen_surface)
        # sprite.draw(self._vscreen_surface)


@RenderingSystem.after_update
def _after_update(self: RenderingSystem, events: list[pg.event.Event], delta_time: int) -> None:
    cam = self._camera_component

    if cam.zoom != self.prev_zoom:
        scaled_surface = pg.transform.scale(cam.vscreen_surface, cam.vscreen_size * cam.zoom)
        self.prev_zoom = cam.zoom
    else:
        scaled_surface = cam.vscreen_surface

    scaled_rect = scaled_surface.get_rect(center=cam.screen.get_rect().center)

    cam.screen.blit(scaled_surface, scaled_rect)
    # if ctx.config.debug:
    #     pg.draw.rect(self._screen, (255, 255, 0), scaled_rect, 1)
