from __future__ import annotations

import typing as t
import uuid
from dataclasses import dataclass, field

from .component import Component, ComponentKey, EntityData


if t.TYPE_CHECKING:
    from .ec_table import EcTable


# TODO: remove ignore when mypy supports 3.12
type EntityUid = str  # type: ignore


def generate_entity_uid() -> EntityUid:
    """Generate an UID for an entity.

    :return: Newly generated entity UID.
    :rtype: EntityUid
    """
    return str(uuid.uuid4()).replace("-", "")


@dataclass(slots=True, frozen=True)
class Entity:
    """Game entity.

    This class provides an OOP interface to underlying :class:`EcTable`
    to make working with entities easier.

    Entity classes are read-only, they cannot be modified or copied.
    """

    uid: EntityUid = field(hash=True)
    _ec_table: EcTable = field(repr=False, hash=False, compare=False)

    @property
    def name(self) -> str:
        """Get entity name."""
        return self._ec_table.get_component(self.uid, EntityData).name  # type: ignore

    def add_component(self, component: Component) -> None:
        """Add a component to an entity.

        :param component: A component to add to an entity.
        :type component: Component

        :raises ComponentsCollisionError: A component with type of
          given component already exists for this entity.
        """
        self._ec_table.add_component(self.uid, component)

    def get_component(self, component_key: ComponentKey) -> Component | None:
        """Get a component instance.

        :param component_key: Key of a component to get.
        :type component: ComponentKey

        :return: A component instance. If component with the given key
          does not exist for this entity, `None` is returned.
        :rtype: Component | None
        """
        return self._ec_table.get_component(self.uid, component_key)

    def remove_component(self, component_key: ComponentKey) -> None:
        """Remove a component from an entity.

        If an entity does not have a component with a given key
        this method will do nothing and immediately return.

        :param component_key: A key of a component to remove.
        :type component_key: ComponentKey

        :raises EntityDataRemovalAttemptError: Removing :class:`EntityData` component
          from an entity is forbidden.
        """
        self._ec_table.remove_component(self.uid, component_key)

    def __iter__(self) -> t.Iterator[Component]:
        """Iterate over entity components.

        :return: Iterator over entity components.
        :rtype: Iterator[Component]
        """
        return self._ec_table.iter_components(self.uid)
