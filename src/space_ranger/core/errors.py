from __future__ import annotations

import typing as t


if t.TYPE_CHECKING:
    from .component import Component, EntityData
    from .entity import Entity


class ComponentsCollisionError(Exception):
    """An exception raised when attempted to add existing component to an entity."""

    def __init__(self, entity: Entity, component: Component) -> None:
        msg = f"Entity [{entity.id}] already has a {component} component"
        super().__init__(msg)


class EntityDataRemovalAttemptError(Exception):
    """An exception raised when trying to remove :class:`EntityData` component from an entity."""

    def __init__(self, entity: Entity) -> None:
        msg = f"Cannot remove {EntityData.__name__} component from entity [{entity.uid}]"
        super().__init__(msg)


class UnknownEntityUidError(Exception):
    """An exception raised when trying to get an entity with unknown UID."""

    def __init__(self, uid: int) -> None:
        msg = f"Entity with the given UID ({uid}) does not exist."
        super().__init__(msg)
