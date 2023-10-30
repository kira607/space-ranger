from __future__ import annotations

import typing as t
from dataclasses import dataclass, field


if t.TYPE_CHECKING:
    from .ecs_manager import EcsManager
    from .entity import Entity
    from .scene import Scene


@dataclass(slots=True)
class Component:
    """Base component for all other components.

    Components are simple "structs" with data, which
    is modified by Systems in runtime.
    """

    _ecs_manager: EcsManager
    _entity_uid: int = field(default=None)

    @property
    def entity(self) -> Entity | None:
        """Get an entity where this component is attached to.

        :return: Entity instance where this component is attached to, if
          the component is not attached to any entity returns None.
        :rtype: Entity | None
        """
        return self._ecs_manager.get_entity_by_uid(self._entity_uid, None)

    @property
    def scene(self) -> Scene:
        """Get a scene where component's entity is instantiated.

        :return: A scene instance. If component is not attached to any entity
          or an entity is not instantiated in any scene returns None.
        :rtype: Scene | None
        """
        return self.entity.scene if self.entity else None

    def get_key(self) -> ComponentKey:
        """Get a component key."""
        return type(self)


type ComponentKey = type[Component]


@dataclass(slots=True)
class EntityData:
    """Entity related data.

    This is a must have entity component
    that each entity has. It cannot be removed
    from an entity. Typically it shoultn't
    be used by Systems directly but they might do if
    it is required to.

    This component holds some basic entity metadata
    related to the game engine itself
    like name, UID, enabled flag, etc.

    This component may be exteded but only if
    new fields relate to engine logic and
    implementation of a separate component doesn't
    make sense in the context of ECS pattern.
    """

    name: str
    uid: int
    enabled: bool = True
