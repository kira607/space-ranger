from __future__ import annotations

import typing as t


if t.TYPE_CHECKING:
    from .component import Component
    from .entity import Entity


class ComponentsCollisionError(Exception):
    """An exception raised when attempted to add existing component to an entity."""

    def __init__(self, entity: Entity, component: Component) -> None:
        msg = f"Entity [{entity.id}] already has a {component} component"
        super().__init__(msg)
