from __future__ import annotations

import typing as t
from dataclasses import dataclass


if t.TYPE_CHECKING:
    from .entity import EntityUid


@dataclass(slots=True)
class Component:
    """Base component.

    Components are simple "structs" with data, which
    is modified by Systems in runtime.

    To create a new component simply inherit from
    base this class and define required component
    fields.

        .. code-block:: python

        @dataclass(slots=True)
        class MyComponent(Component):
            speed: float = 0.0
            max_speed: float = 5.0
            is_jumping: bool = False

    Some recomendations for component definition:

    * Use slotted dataclass. It will make components
        faster and easier to create.

    * Do not define any methods. The sole purpose
        of components is to store data. The processing of
        this data is indendent to be implemented in systems.
    """

    @classmethod
    def get_key(cls) -> ComponentKey:
        """Get a component key.

        :return ComponentKey: A component key.
        """
        return cls


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
    uid: EntityUid
    enabled: bool = True
