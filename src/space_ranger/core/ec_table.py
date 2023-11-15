from __future__ import annotations

import typing as t

from .component import Component, ComponentKey, EntityData
from .entity import Entity, EntityUid, generate_entity_uid
from .errors import ComponentsCollisionError, EntityDataRemovalAttemptError, UnknownEntityUidError
from .utils import MISSING


class EcTable:
    """Entity-component table.

    This class provides an interface to
    a table where :class:`Component` objects
    are stored and associated with an entity.

    The table structure is:
    - Each row of the table is an entity.
    - First column is the entity UID.
    - Other columns are components keys.
    - A cell contains a :class:`Component` instance (or None).

    Here is how an example table looks like:

    Entity UID | ComponentA   | ComponentB   | ... | ComponentX   |
    -----------|--------------|--------------|-----|--------------|
    EntityUid1 | ComponentA() | ComponentB() | ... | None         |
    EntityUid2 | ComponentA() | None         | ... | ComponentX() |
    ...        | ...          | ...          | ... | ...          |
    EntityUidN | None         | None         | ... | ComponentX() |
    """

    def __init__(self) -> None:
        self._table: dict[EntityUid, dict[ComponentKey, Component]] = {}

    # Entity

    def create_entity(self, name: str, *components: Component) -> Entity:
        """Create a new entity with a given set of components.

        :param str name: Name of the entity.
        :param Component components: List of components to be added to the entity.

        :return Entity: New entity.
        """
        uid = generate_entity_uid()

        # avoid UID collisions
        # the check works in O(1) so this should be OK
        # as long as UID generator doesn't create too many collisions.
        while self._table.get(uid) is not None:
            uid = generate_entity_uid()

        self._table[uid] = {EntityData: EntityData(name, uid)}  # type: ignore

        for component in components:
            self.add_component(uid, component)

        return self.get_entity_by_uid(uid)

    def get_entity_by_uid(self, uid: EntityUid, default: t.Any = MISSING) -> Entity | t.Any:
        """Get an entity by its UID.

        :param EntityUid uid: Entity UID
        :param t.Any default: A default value to return if entity with given
            UID does not exist, defaults to MISSING.

        :raises UnknownEntityUidError: Entity with the given UID does not exist and
            a default value was not provided.

        :return Entity | t.Any: Entity instance if found one, default otherwise.
            If default value was not provided an :class:`UnknownEntityUidError`
            exception is raised.
        """
        entity = self._table.get(uid, MISSING)
        if entity is MISSING:
            if default is MISSING:
                raise UnknownEntityUidError(uid)
            return default
        return Entity(uid, self)

    def delete_entity(self, uid: EntityUid) -> None:
        """Delete an entity by its UID.

        Deliton of an entity will cause the loss
        of all of its data and components.

        :param EntityUid uid: Entity UID to delete.

        :raises UnknownEntityUidError: Entity with the given UID does not exist.
        """
        if uid not in self._table:
            raise UnknownEntityUidError(uid)
        del self._table[uid]

    # Component

    def add_component(self, entity_uid: EntityUid, component: Component) -> None:
        """Add a component to an entity.

        :param EntityUid entity_uid: UID of an entity to add a component to.
        :param Component component: A component to add to an entity.

        :raises ComponentsCollisionError: A component with type of
            given component already exists for this entity.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        entity = self.get_entity_by_uid(entity_uid)
        key = component.get_key()

        if self.get_component(entity_uid, key):
            raise ComponentsCollisionError(entity, component)

        self._table[entity_uid][key] = component

    def get_component(self, entity_uid: EntityUid, component_key: ComponentKey) -> Component | None:
        """Get a component instance by the given `entity_uid` and `component_key`.

        :param EntityUid entity_uid: Entity UID that holds the component.
        :param ComponentKey component_key: Key of a component to get.

        :return Component | None: Component instance. If entity with given `entity_uid` does not exist
            or it does not contain a component with the given `component_key`
            returns `None`.
        """
        return self._table.get(entity_uid, {}).get(component_key)

    def remove_component(self, entity_uid: EntityUid, component_key: ComponentKey) -> None:
        """Remove a component from an entity.

        If an entity with the given UID exists
        and it does not have a component with a given key
        this method will do nothing and immediately return.

        :param EntityUid entity_uid: UID of an entity from which a component must be removed.
        :param ComponentKey component_key: A key of a component to remove.

        :raises UnknownEntityUidError: Entity with the given UID does not exist.
        :raises EntityDataRemovalAttemptError: Removing :class:`EntityData` component
            from an entity is forbidden.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        entity = self.get_entity_by_uid(entity_uid)

        # component existance check
        if self.get_component(entity_uid, component_key) is None:
            return

        if component_key == EntityData:  # type: ignore[comparison-overlap]
            raise EntityDataRemovalAttemptError(entity)

        del self._table[entity_uid][component_key]

    # Iterators

    def iter_entities(self) -> t.Iterator[Entity]:
        """Iterate over entities.

        :return Iterator[Entity]: Iterator over entities.
        """
        return iter((self.get_entity_by_uid(uid) for uid in self._table))

    def iter_components(self, uid: EntityUid) -> t.Iterator[Component]:
        """Iterate over entity components.

        :param EntityUid entity_uid: UID of an entity over which components to iterate.

        :raises UnknownEntityUidError: Entity with the given UID does not exist.

        :return Iterator[Component]: Iterator over entity components.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        self.get_entity_by_uid(uid)
        return iter((self.get_component(uid, key) for key in self._table[uid]))  # type: ignore

    # Quering entities

    def get_entities(self) -> list[Entity]:
        """Get a list of entities.

        :return list[Entity]: A list of entities.
        """
        return list(self.iter_entities())

    def get_entities_by_components(
        self,
        *components_keys: ComponentKey,
        partitial: bool = False,
    ) -> set[Entity]:
        """Get entities set matching given components keys list.

        :param ComponentKey components_keys: Components keys that entity should match.
        :param bool partitial: If `True`, will require an entity match all `components_keys`,
            otherwise will require an entity to match at least one of `components_keys`.

        :return set[Entity]: Set of entities matching given components.
        """
        match_f = any if partitial else all
        return {e for e in self.iter_entities() if match_f((e.get_component(k) for k in components_keys))}
