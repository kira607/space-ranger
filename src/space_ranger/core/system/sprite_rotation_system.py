from collections import defaultdict

import pygame as pg

from space_ranger.core.component import Sprite
from space_ranger.core.entity import Entity

from ._system import System


class SpriteRotationSystem(System):
    """A system for rotating :class:`space_ranger.core.component.Sprite` components."""

    def __init__(self, group: int = 0) -> None:
        super().__init__(group)
        self.rotation_precision = 0.5
        self.rotations_cache: dict[int, dict[int, tuple[pg.Surface, pg.Rect]]] = defaultdict(dict)

    def _match_entity(self, entity: Entity) -> bool:
        required_components = {Sprite}
        if entity.match(*required_components):
            return required_components
        return set()


@SpriteRotationSystem.update_entity
def _update_component(self: SpriteRotationSystem, entity_id: int, events: list[pg.event.Event], delta_time: int) -> None:
    sprite = self.queued_entities[entity_id][Sprite]
    transform = sprite.entity.transform
    rotation = -int(transform.rotation)

    img, rct = self.rotations_cache.get(sprite.entity.id, {}).get(rotation, (None, None))
    if img is None:
        img = pg.transform.rotate(sprite.source, rotation)
        rct = img.get_rect()
        self.rotations_cache[sprite.entity.id][rotation] = img, rct

    sprite.image = img
    sprite.rect = rct
    sprite.rect.center = transform.position
