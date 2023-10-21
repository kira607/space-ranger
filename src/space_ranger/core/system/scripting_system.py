import pygame as pg

from space_ranger.core.component import Script
from space_ranger.core.entity import Entity

from ._system import System


class ScriptingSystem(System):
    """A system handling entities with :class:`space_ranger.core.component.Script` component."""

    def _match_entity(self, entity: Entity) -> bool:
        result = set()
        required_components_classes = {Script}
        for component_class in required_components_classes:
            for component_key in entity.components:
                if issubclass(component_key, component_class):
                    result.add(component_key)
        return result


@ScriptingSystem.start_entity
def _start_entity(self: ScriptingSystem, entity_id: int) -> None:
    scripts = self.queued_entities[entity_id]
    for _, script in scripts.items():
        script.start()


@ScriptingSystem.update_entity
def _update_entity(self: ScriptingSystem, entity_id: int, events: list[pg.event.Event], delta_time: int) -> None:
    scripts = self.queued_entities[entity_id]
    for _, script in scripts.items():
        script.update(events, delta_time)
