from __future__ import annotations

import typing as t
from dataclasses import dataclass, field

from .component import Component, ComponentKey, Transform
from .errors import ComponentsCollisionError


if t.TYPE_CHECKING:
    from .scene import Scene


class EntityIdGenerator:
    """An ID generator for entities."""

    _current = -1

    @classmethod
    def generate_next_id(cls) -> int:
        """Generate an ID for an entity.

        :return: Newly generated entity ID
        :rtype: int
        """
        cls._current += 1
        return cls._current


# TODO: add logic for updating systems when entity components are changed (added, removed)
@dataclass(slots=True)
class Entity:
    """Base entity."""

    name: str
    id: int = field(default_factory=EntityIdGenerator.generate_next_id, compare=True)  # noqa: A003
    scene: Scene = field(default=None, compare=False)
    components: [dict[ComponentKey, Component]] = field(default_factory=dict, compare=True)

    @property
    def transform(self) -> Transform:
        """Get a transform component."""
        return self.get_component(Transform)

    def match(self, *components_keys: ComponentKey) -> bool:
        """Check if an entity has all of required components.

        :return: `True` if entity has components of all
          given types, `False` otherwise.
        :rtype: bool
        """
        return all((self.get_component(k) for k in components_keys))

    def get_component(self, component_key: ComponentKey) -> Component | None:
        """Get an entity component.

        :param component_key: A type of component to get
        :type component: ComponentKey

        :return: A component instance if component of given type
          exists for this entity, None otherwise.
        :rtype: Component | None
        """
        return self.components.get(component_key)

    def add_component(self, component: Component) -> None:
        """Add a component to an entity.

        :param component: A component to add to an entity.
        :type component: Component

        :raises ComponentsCollisionError: A component with type of
          given component already exists for this entity.
        """
        key = component.get_key()
        if self.get_component(key):
            raise ComponentsCollisionError(self, component)
        self.components[key] = component
        component._entity = self

    def remove_component(self, component_key: ComponentKey) -> None:
        """Remove a component from entity.

        .. warning::
            The function may raise a `KeyError` if a component
            with the given key does not exist for this entity.
        """
        del self.components[component_key]

    def __hash__(self) -> int:
        """Get entity hash value.

        :return: Entity hash value.
        :rtype: int
        """
        return hash(self.id)


def make_entity(name: str, *components: Component) -> Entity:
    """Create a new entity with a given set of components.

    Automatically adds a :class:`Transform` component
    if wasn't provided one.

    :param name: Name of the entity.
    :type name: str

    :return: New entity.
    :rtype: Entity
    """
    e = Entity(name)

    for component in components:
        e.add_component(component)

    if e.get_component(Transform) is None:
        e.add_component(Transform())

    return e
