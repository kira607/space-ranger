from __future__ import annotations

import typing as t
from dataclasses import dataclass, field


if t.TYPE_CHECKING:
    from space_ranger.core.entity import Entity
    from space_ranger.core.scene import Scene


@dataclass(slots=True)
class Component:
    """Base component for all other components."""

    _entity: Entity = field(default=None)

    @property
    def entity(self) -> Entity | None:
        """Get an entity where this component is attached to."""
        return self._entity

    @property
    def scene(self) -> Scene:
        """Get a scene where entity is instantiated."""
        return self._entity.scene

    def get_key(self) -> ComponentKey:
        """Get a component key."""
        return type(self)


type ComponentKey = type[Component]
