from __future__ import annotations

import typing as t

import pygame as pg

from space_ranger.core.component import Component, ComponentKey
from space_ranger.core.entity import Entity


if t.TYPE_CHECKING:
    from space_ranger.core.scene import Scene


# TODO: extract entities queue collection in a separate class (e.g. `SystemEntitiesQueue`)
class System:
    """Base system.

    :var str id: System ID.
    :var Scene scene: A scene in which this system is working.
    :var int group: A system group. The higher the group, the later
      a system will be updated.
    :var dict[int, Entity] queued_entities: A collection of entities
      that are processed by this system.

    :param group: System processing group.
    :type group: int
    """

    # start hooks
    _before_start = None
    _start_entity = None
    _after_start = None

    # update hooks
    _before_update = None
    _update_entity = None
    _after_update = None

    def __init__(self, group: int = 0) -> None:
        self.id: str = self.__class__.__name__  # noqa: A003
        self.scene: Scene = None
        self.group: int = group
        self.queued_entities: dict[int, dict[ComponentKey, Component]] = {}

    def queue_entity(self, entity: Entity) -> bool:
        """Queue an entity for processing.

        Before queueing this method will check if a given entity
        has all required components.

        :param entity: An entity to queue for processing.
        :type entity: Entity

        :return: `True` if entity has all required components and
          is queued for processing, `False` otherwise.
        :rtype: bool
        """
        matched_components_keys = self._match_entity(entity)
        if matched_components_keys:
            self._queue_entity(entity, matched_components_keys)
            if self._start_entity:
                self._start_entity(entity.id)
        return bool(matched_components_keys)

    def remove_entity(self, entity: Entity) -> None:
        """Remove entity from processing queue.

        .. warning::
            The function may raise a `KeyError` if an entity
            with the given id does not exist for this system.

        :param entity: Entity to remove.
        :type entity: Entity
        """
        del self.queued_entities[entity.id]

    def contains_entity(self, entity: Entity) -> bool:
        """Check if an entity is queued for processing in this system.

        :param entity: Entity instance to check.
        :type entity: Entity

        :return: `True` if given entity is queued for processing, `False` otherwise.
        :rtype: bool
        """
        return bool(self.queued_entities.get(entity.id))

    def start(self) -> None:
        """Start system up.

        This will start all queued entities.
        """
        if self._before_start:
            self._before_start()

        if self._start_entity:
            for entity_id in self.queued_entities:
                self._start_entity(entity_id)

        if self._after_start:
            self._after_start()

    def update(self, events: list[pg.event.Event], delta_time: int) -> None:
        """Run system update.

        This will update all queued entities.

        :param events: List of pygame events to process.
        :type events: list[pg.event.Event]
        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        if self._before_update:
            self._before_update(events, delta_time)

        if self._update_entity:
            for entity_id in self.queued_entities:
                self._update_entity(entity_id, events, delta_time)

        if self._after_update:
            self._after_update(events, delta_time)

    @classmethod
    def before_start(cls, f: t.Callable[[System], None]) -> None:
        """Assign a hook for overall system startup.

        `before_start` hook function is called
        at the beginning of the system startup.

        Required hook function parameters:

            - `self`

        :param f: A `before_start` hook function.
        :type f: Callable[[System], None]
        """
        cls._before_start = f

    @classmethod
    def start_entity(cls, f: t.Callable[[System, int], None]) -> None:
        """Assign a hook for entity specific startup.

        `start_entity` hook function is called
        for each entity in the scene at the system
        startup and once per entity when it's queued
        for processing.

        Required hook function parameters:

            - `self`
            - `entity_id` - An entity ID.

        :param f: A `start_entity` hook function.
        :type f: Callable[[System, int], None]
        """
        cls._start_entity = f

    @classmethod
    def after_start(cls, f: t.Callable[[System], None]) -> None:
        """Assign a hook for overall system post startup.

        `after_start` hook function is called
        at the end of the system startup.

        Required hook function parameters:

            - `self`

        :param f: A `after_start` hook function.
        :type f: Callable[[System], None]
        """
        cls._after_start = f

    @classmethod
    def before_update(cls, f: t.Callable[[System, list[pg.event.Event], int], None]) -> None:
        """Assign a hook for overall system update.

        `before_update` hook function is called
        once per frame at the start of system update.

        Required hook function parameters:

            - `self`
            - `events` - List of pygame events to process.
            - `delta_time` - Frame delta time (in milliseconds).

        :param f: `before_update` hook function.
        :type f: Callable[[System, list[pg.event.Event], int], None]
        """
        cls._before_update = f

    @classmethod
    def update_entity(cls, f: t.Callable[[System, int, list[pg.event.Event], int], None]) -> None:
        """Assign a hook for entity specific update.

        `update_entity` hook function is called
        once per frame for each queued entity.

        Required hook function parameters:

            - `self`
            - `entity_id` - An entity ID.
            - `events` - List of pygame events to process.
            - `delta_time` - Frame delta time (in milliseconds).

        :param f: `update_entity` hook function.
        :type f: Callable[[System, int, list[pg.event.Event], int], None]
        """
        cls._update_entity = f

    @classmethod
    def after_update(cls, f: t.Callable[[System, list[pg.event.Event], int], None]) -> None:
        """Assign a hook for overall system post update.

        `after_update` hook function is called
        once per frame at the end of system update.

        Required hook function parameters:

            - `self`
            - `events` - List of pygame events to process.
            - `delta_time` - Frame delta time (in milliseconds).

        :param f: `after_update` hook function.
        :type f: Callable[[System, list[pg.event.Event], int], None]
        """
        cls._after_update = f

    def _match_entity(self, entity: Entity) -> set[ComponentKey]:
        """Check if the given entity matches this system by its components.

        :return: A set of components keys that match this system.
          If return set is empty, given entity doesn't match this
          system and it won't be queued for processing.
        :rtype: set[ComponentKey]
        """
        return set()

    def _queue_entity(self, entity: Entity, components_keys: set[ComponentKey]) -> None:
        self.queued_entities[entity.id] = {}
        for key in components_keys:
            self.queued_entities[entity.id][key] = entity.get_component(key)

    def __hash__(self) -> int:
        """Get system hash value."""
        return hash(self.id)
