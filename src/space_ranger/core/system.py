from __future__ import annotations

import typing as t

from .component import ComponentKey
from .entity import Entity


if t.TYPE_CHECKING:
    from .ecs_manager import EcsManager
    from .scene import Scene


type SystemExecutor = t.Callable[[Scene, Entity], None]


class System:
    """Base system.

    System can be of one of two types:

    1. Startup system - runs once at a scene startup for each compatible entity.
    2. Setup system - runs once at entity instantiation for each compatible entity.
    2. Update system - runs once per frame for each compatible entity.

    System has a set of required components
    that is used to efficently parallelalize
    multiple systems.

    Systems with overlaping components run sequantially.
    Systems with no overlaping components can run in parallel.
    It is assumed that systems will do both read and write
    operations to required components.
    """

    def __init__(self, name: str, executor: SystemExecutor, *required_components: ComponentKey) -> None:
        self._name = name
        self._executor = executor
        self._required_components = set(required_components)
        self._ecs_manager: EcsManager = None
        self._entities: set[int] = set()

    def match_entity(self, entity_uid: int) -> bool:
        """Check if an entity matches this system by its components.

        Entity matches a system when it has all of the components
        that are required by a system. Entity can have more components
        that are required, but never less.

        :param entity_uid: UID of an entity to check for compatibility.
        :type entity_uid: int

        :return: True, if the entity matches this system, False otherwise.
        :rtype: bool
        """
        return all(
            self._ecs_manager.get_component(entity_uid, component_key) is not None
            for component_key in self._required_components
        )

    def add_entity(self, entity_uid: int) -> None:
        """Add an entity to the system processing queue.

        :param entity_uid: UID of entity to add for processing.
        :type entity_uid: int
        """
        self._entities.add(entity_uid)

    def remove_entity(self, entity_uid: int) -> None:
        """Remove an entity from the system processing queue.

        :param entity_uid: UID of entity to remove from processing.
        :type entity_uid: int
        """
        self._entities.remove(entity_uid)

    def update_entities(self) -> None:
        """Update entities processing queue.

        Queries EcsManager for compatible entities and
        updates processing queue.
        """
        self._entities = {entity.uid for entity in self._ecs_manager.iter_entities() if self.match_entity(entity.uid)}

    def run(self) -> None:
        """Run a system."""
        for entity_uid in self._entities:
            self._executor(
                self._ecs_manager.scene,
                self._ecs_manager.get_entity_by_uid(entity_uid),
            )
