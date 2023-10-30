from __future__ import annotations

import typing as t
import uuid
from dataclasses import dataclass, field

from .component import Component, ComponentKey, EntityData


if t.TYPE_CHECKING:
    from .ecs_manager import EcsManager
    from .scene import Scene


class EntityUidGenerator:
    """An UID generator for entities."""

    @classmethod
    def generate_next_id(cls) -> int:
        """Generate an UID for an entity.

        :return: Newly generated entity UID.
        :rtype: int
        """
        return uuid.uuid4().int


@dataclass(slots=True, frozen=True)
class Entity:
    """Game entity.

    This class provides an OOP interface to underlying ECS registry,
    where all data about Entities, Components, and Systems is stored.

    Entity classes are read-only, they cannot be modified or copied.
    """

    _ecs_manager: EcsManager = field(repr=False, hash=False)
    uid: int = field(hash=True)

    @property
    def name(self) -> str:
        """Get a name of the entity."""
        return self._ecs_manager.get_component(EntityData).name

    @property
    def scene(self) -> Scene | None:
        """Get a scene where entity is instantiated.

        :return: A scene instance. If the entity is not instantiated in any
          scene returns None.
        :rtype: Scene | None
        """
        return self._ecs_manager.scene

    def add_component(self, component: Component) -> None:
        """Add a component to an entity.

        :param component: A component to add to an entity.
        :type component: Component

        :raises ComponentsCollisionError: A component with type of
          given component already exists for this entity.
        """
        self._ecs_manager.add_component(self.uid, component)

    def get_component(self, component_key: ComponentKey) -> Component | None:
        """Get a component instance.

        :param component_key: Key of a component to get.
        :type component: ComponentKey

        :return: A component instance. If component with the given key
          does not exist for this entity, `None` is returned.
        :rtype: Component | None
        """
        return self._ecs_manager.get_component(self.uid, component_key)

    def remove_component(self, component_key: ComponentKey) -> None:
        """Remove a component from an entity.

        If an entity does not have a component with a given key
        this method will do nothing and immediately return.

        :param component_key: A key of a component to remove.
        :type component_key: ComponentKey

        :raises EntityDataRemovalAttemptError: Removing :class:`EntityData` component
          from an entity is forbidden.
        """
        self._ecs_manager.remove_component(self.uid, component_key)

    def __iter__(self) -> t.Iterator[Component]:
        """Iterate over entity components.

        :return: Iterator over entity components.
        :rtype: Iterator[Component]
        """
        return self._ecs_manager.iter_components(self.uid)
