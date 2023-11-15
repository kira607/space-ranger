from __future__ import annotations

import typing as t


if t.TYPE_CHECKING:
    from .component import Component, EntityData
    from .entity import Entity, EntityUid


class ComponentsCollisionError(Exception):
    """An exception raised when attempted to add existing component to an entity."""

    def __init__(self, entity: Entity, component: Component) -> None:
        msg = f"Entity [{entity.uid}] already has a {component} component"
        super().__init__(msg)


class EntityDataRemovalAttemptError(Exception):
    """An exception raised when trying to remove :class:`EntityData` component from an entity."""

    def __init__(self, entity: Entity) -> None:
        msg = f"Cannot remove {EntityData.__name__} component from entity [{entity.uid}]"
        super().__init__(msg)


class UnknownEntityUidError(Exception):
    """An exception raised when trying to get an entity with unknown UID."""

    def __init__(self, uid: EntityUid) -> None:
        msg = f"Entity with the given UID ({uid}) does not exist."
        super().__init__(msg)


class SystemExecutorIsNotCallableError(Exception):
    """An exception raised when a system executor is not a callable object."""

    def __init__(self, system_executor: t.Any) -> None:
        msg = f"A system executor ({system_executor}) is not a callable object."
        super().__init__(msg)


class UnknownSceneIdError(Exception):
    """An exception raised when trying to switch to a scene with unknown id."""

    def __init__(self, scene_id: str) -> None:
        msg = f"Unknown scene id: {scene_id}."
        super().__init__(msg)
