from __future__ import annotations

import pygame as pg

from ._ctx import ctx
from .component import Camera, ComponentKey
from .entity import Entity, make_entity
from .logging import LoggerMixin
from .system import RenderingSystem, ScriptingSystem, System


# TODO: extract entities collection logic in a separate class (e.g. `EntitiesManager`)
# TODO: extract systems collection logic in a separate class (e.g. `SystemsManager`)


class Scene(LoggerMixin):
    """An application scene.

    Acts like a usual pygame event loop.

    A scene subclasses should never be inherited.

    Provides with methods to override to control the loop:
    * `_start()` - initialize scene
    * `_process_event(self, event: pg.event.Event)` - process event
    * `_update(self, delta_time: int)` - update
    * `_draw(self, screen: pg.Surface)` - draw
    """

    def __init__(self, scene_id: str) -> None:
        # some base stuff for state handling
        self._id = str(scene_id)
        self._done = False
        self._quit = False
        self._previous: str | None = None
        self._next: str | None = None

        self._entities: set[Entity] = set()
        self._systems: set[System] = set()

        # systems
        self.rendering_system: RenderingSystem
        self.scripting_system: ScriptingSystem

    @property
    def id(self) -> str:  # noqa: A003
        """A scene id."""
        return self._id

    @property
    def is_done(self) -> bool:
        """A flag indicating whether a scene is finished."""
        return self._done

    @property
    def is_app_should_quit(self) -> bool:
        """A flag indicating whether the app shoud be stopped."""
        return self._quit

    @property
    def previous(self) -> str | None:
        """A previous scene id."""
        return self._previous

    @previous.setter
    def previous(self, value: str) -> None:
        self._previous = value

    def switch_scene(self, next_scene_id: str) -> None:
        """Tell application to switch to another scene.

        This will finish up current scene.

        :param next_scene_id: Id of a scene to switch to.
        :type next_scene_id: str
        """
        self._next = next_scene_id
        self._done = True

    def exit_application(self) -> None:
        """Exit application."""
        self._quit = True

    def get_next_scene(self) -> str:
        """Get a next scene id."""
        if self._next is None:
            raise RuntimeError("Next scene id is not set!")
        return self._next

    def instantiate(self, entity: Entity) -> None:
        """Instantiate an entity in the scene.

        This also will queue an entity for updates
        in all required systems.

        :param entity: An entity to instantiate.
        :type entity: Entity
        """
        self._entities.add(entity)
        for system in self._systems:
            system.queue_entity(entity)

    def destroy(self, entity: Entity) -> None:
        """Destroy and entity.

        This also will remove and entity
        from all systems where it is queued for updates.

        :param entity: An entity to destroy.
        :type entity: Entity
        """
        self._entities.remove(entity)
        for system in self._systems:
            if system.contains_entity(entity):
                system.remove_entity(entity)

    def find_entities(self, *components_keys: ComponentKey) -> set[Entity]:
        """Query for entities matching required components."""
        result = set()
        for e in self._entities:
            if e.match(*components_keys):
                result.add(e)
        return result

    def start(self) -> None:
        """Do a scene statup.

        This method is called before the fisrt game loop iteration.
        """
        scene_name_log = f"{self.__class__.__name__}('{self.id}')"
        self.logger.info(f"Starting up {scene_name_log} scene...")

        self.logger.info(f"{scene_name_log} | Collecting entities...")
        # self._entities.add(make_entity(Camera(screen=ctx.screen.surface)))
        self._collect_entities()
        self.logger.info(f"{scene_name_log} | Collected {len(self._entities)} {"entity" if len(self._entities) == 1 else "entities"}")

        self.logger.info(f"{scene_name_log} | Collecting systems...")
        self._collect_systems()
        self.logger.info(f"{scene_name_log} | Collected {(len(self._systems))} {"system" if len(self._systems) == 1 else "systems"}...")

        self.logger.info(f"{scene_name_log} | Starting entities...")
        # instantiation of entities will automatically queue them for appropriate systems
        for e in self._entities:
            self.instantiate(e)
        self.logger.info(f"{scene_name_log} | Starting entities | DONE")

        self.logger.info(f"{scene_name_log} | Systems info:")
        for system in self._systems:
            self.logger.info(f"{scene_name_log} | {system.id} | queued entities: {len(system.queued_entities)}")

        self.logger.info(f"{scene_name_log} | Starting systems...")
        for system in self._systems:
            system.start()
        self.logger.info(f"{scene_name_log} | Starting systems | DONE")

        self._start()

    def update(self, events: list[pg.event.Event], delta_time: int) -> None:
        """Update scene.

        :param events: List of pygame events to process.
        :type events: list[pg.event.Event]
        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        for system in self._systems:
            system.update(events, delta_time)
        self._update(events, delta_time)

    def draw(self, screen: pg.Surface) -> None:
        """Draw scene on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        self._draw(screen)

    def finish(self) -> None:
        """Do a scene cleanup.

        This method is called after a last frame
        before scene switch or application shutdown.
        """
        self.logger.info(f"Cleaning up '{self.id}' scene...")
        self._done = False
        self._finish()

    def _start(self) -> None:
        """Do a scene statup.

        This method is called before the fisrt game loop iteration.
        """
        pass

    def _update(self, events: list[pg.event.Event], delta_time: int) -> None:
        """Update scene.

        :param events: List of pygame events to process.
        :type events: list[pg.event.Event]
        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        pass

    def _draw(self, screen: pg.Surface) -> None:
        """Draw scene on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        pass

    def _finish(self) -> None:
        """Do a scene cleanup.

        This method is called after a last frame
        before scene switch or application shutdown.
        """
        pass

    def _collect_entities(self) -> None:
        user_defined_entities = self._get_entities()
        self._entities.update(user_defined_entities)
        for entity in self._entities:
            entity.scene = self

    def _get_entities(self) -> set[Entity]:
        return set()

    def _collect_systems(self) -> None:
        user_defined_systems = self._get_systems()
        self._systems.update(user_defined_systems)
        for system in self._systems:
            system.scene = self

    def _get_systems(self) -> set[System]:
        return set()
