import typing as t

from .component import Component, ComponentKey
from .entity import Entity, EntityData, EntityUidGenerator
from .errors import ComponentsCollisionError, EntityDataRemovalAttemptError, UnknownEntityUidError
from .system import System
from .utils import MISSING


if t.TYPE_CHECKING:
    from .scene import Scene


class EcsManager:
    """ECS manager.

    The manager keeps track of all ECS entities.

    Entities and Components are organized in a table:

    Entity UID | Component Key 1     | Component Key 2     | ... | Component Key n     |
    -----------|---------------------|---------------------|-----|---------------------|
    8482938582 | ComponentInstance() | ComponentInstance() | ... | None                |
    9957299958 | ComponentInstance() | None                | ... | ComponentInstance() |
    1693902858 | None                | None                | ... | ComponentInstance() |
    ...        | ...                 | ...                 | ... | ...                 |

    Systems are simply stored in a map with `(system_name -> system)` pairs.

    :param scene: The scene.
    :type scene: Scene
    """

    def __init__(self, scene: Scene | None = None) -> None:
        self.scene = scene
        self.entity_component_table: dict[int, dict[ComponentKey, Component]] = {}
        self.systems: set[System] = set()

    # Entity

    def create_entity(self, name: str, *components: Component) -> Entity:
        """Create a new entity with a given set of components.

        :param name: Name of the entity.
        :type name: str
        :param components: List of components to be added to the entity.
        :type components: Component

        :return: New entity.
        :rtype: Entity
        """
        uid = EntityUidGenerator.generate_next_id()

        # avoid UID collisions
        # the check works in O(1) so this should be OK
        # as long as UID generator doesn't create too many collisions.
        while self.entity_component_table.get(uid) is not None:
            uid = EntityUidGenerator.generate_next_id()

        self.entity_component_table[uid] = {EntityData.get_key(): EntityData(name, uid)}

        for component in components:
            self.add_component(uid, component)

        # here a required components could be added to the entity.
        # not sure if it is needed right now...
        # if entity.get_component(Transform) is None:
        #     entity.add_component(Transform())

        return self.get_entity_by_uid(uid)

    def get_entity_by_uid(self, uid: int, default: t.Any = MISSING) -> Entity | t.Any:
        """Get an entity by its UID.

        :param uid: Entity UID
        :type uid: int

        :raises UnknownEntityUidError: Entity with the given UID does not exist and
          a default value was not provided.

        :return: Entity instance if found one, default otherwise.
          If default value was not provided an exception is raised.
        :rtype: Entity | None
        """
        entity = self.entity_component_table.get(uid, default)
        if entity is MISSING:
            raise UnknownEntityUidError(uid)
        return Entity(self, uid)

    def delete_entity(self, uid: int) -> None:
        """Delete an entity by its UID.

        Deliton of an entity will cause the loss
        of all of its data and components.

        :param uid: Entity UID to delete.
        :type uid: int

        :raises UnknownEntityUidError: Entity with the given UID does not exist.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        self.get_entity_by_uid(uid)
        del self.entity_component_table[uid]

    # Component

    def add_component(self, entity_uid: int, component: Component) -> None:
        """Add a component to an entity.

        :param entity_uid: UID of an entity to add a component to.
        :type entity_uid: int
        :param component: A component to add to an entity.
        :type component: Component

        :raises UnknownEntityUidError: Entity with the given UID does not exist.
        :raises ComponentsCollisionError: A component with type of
          given component already exists for this entity.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        entity = self.get_entity_by_uid(entity_uid)
        key = component.get_key()

        if self.get_component(entity_uid, key):
            raise ComponentsCollisionError(entity, component)

        self.entity_component_table[entity_uid][key] = component
        component._ecs_manager = self
        component._entity_uid = entity_uid

    def get_component(self, entity_uid: int, component_key: ComponentKey) -> Component | None:
        """Get a component instance by the given `entity_uid` and `component_key`.

        :param entity_uid: Entity UID that holds the component.
        :type entity_uid: int
        :param component_key: Key of a component to get.
        :type component_key: ComponentKey

        :return: Component instance. If entity with given `entity_uid` does not exist
          or it does not contain a component with the given `component_key`
          returns `None`.
        :rtype: Component | None
        """
        return self.entity_component_table.get(entity_uid, {}).get(component_key)

    def remove_component(self, entity_uid: int, component_key: ComponentKey) -> None:
        """Remove a component from an entity.

        If an entity with the given UID exists
        and it does not have a component with a given key
        this method will do nothing and immediately return.

        :param entity_uid: UID of an entity from which a component must be removed.
        :type entity_uid: int
        :param component_key: A key of a component to remove.
        :type component_key: ComponentKey

        :raises UnknownEntityUidError: Entity with the given UID does not exist.
        :raises EntityDataRemovalAttemptError: Removing :class:`EntityData` component
          from an entity is forbidden.
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        self.get_entity_by_uid(entity_uid)

        # component existance check
        if self.get_component(entity_uid, component_key) is None:
            return

        if component_key == EntityData:
            raise EntityDataRemovalAttemptError(self)

        del self.entity_component_table[entity_uid][component_key]

    # System

    def add_system(self, system: System) -> None:
        """Add a system.

        :param system: A system instance to add.
        :type system: System
        """
        self.systems.add(system)
        system._ecs_manager = self

    # Iterators

    def iter_entities(self) -> t.Iterator[Entity]:
        """Iterate over entities.

        :return: Iterator over entities.
        :rtype: Iterator[Entity]
        """
        return iter((self.get_entity_by_uid(uid) for uid in self.entity_component_table))

    def iter_components(self, uid: int) -> t.Iterator[Component]:
        """Iterate over entity components.

        :param entity_uid: UID of an entity over which components to iterate.
        :type entity_uid: int

        :raises UnknownEntityUidError: Entity with the given UID does not exist.

        :return: Iterator over entity components.
        :rtype: Iterator[Component]
        """
        # below line invokes an UID check and might raise UnknownEntityUidError
        self.get_entity_by_uid(uid)
        return iter((self.get_component(uid, key) for key in self.entity_component_table[uid]))

    def iter_systems(self) -> t.Iterator[System]:
        """Iterate over systems.

        :return: Iterator over systems.
        :rtype: t.Iterator[System]
        """
        return iter(self.systems)

    # Quering entities

    def get_entities(self) -> list[Entity]:
        """Get a list of entities.

        :return: A list of entities.
        :rtype: list[Entity]
        """
        return list(self.iter_entities())

    def get_entities_by_components(
        self,
        *components_keys: ComponentKey,
        partitial: bool = False,
    ) -> set[Entity]:
        """Get entities set matching given components keys list.

        :param components_keys: Components keys that entity should match.
        :type components_keys: ComponentKey
        :param partitial: If `True`, will require an entity match all `components_keys`,
          otherwise will require an entity to match at least one of `components_keys`.
        :type partitial: bool

        :return: Set of entities matching given components.
        :rtype: set[Entity]
        """
        match_f = any if partitial else all
        return {e for e in self.iter_entities() if match_f((e.get_component(k) for k in components_keys))}
