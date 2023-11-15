from __future__ import annotations

import typing as t

from .component import Component, ComponentKey
from .ec_table import EcTable
from .entity import Entity
from .logging import LoggerMixin
from .system import SystemExecutor, SystemsPipeline, SystemsSchedule, make_system


if t.TYPE_CHECKING:
    from .application import Application


class Scene(LoggerMixin):
    """An application scene.

    :param str name: The name of the scene.
    """

    def __init__(self, scene_name: str) -> None:
        self._name = str(scene_name)
        self._app: Application
        self._ec_table = EcTable()
        self._systems_schedule: SystemsSchedule = SystemsSchedule()

    @property
    def name(self) -> str:
        """A scene name."""
        return self._name

    def add_entity(self, entity_name: str, *components: Component) -> Entity:
        """Add an entity the a scene.

        :param str entity_name: The name of the entity.
        :param Component components: List of components to attach to the entity.

        :return Entity: Entity instance.
        """
        entity = self._ec_table.create_entity(entity_name, *components)
        entity_uid = entity.uid
        for pipeline in (self._systems_schedule.start, self._systems_schedule.update):
            for system in pipeline._systems:
                if system.match_entity(entity_uid):
                    system.add_entity(entity_uid)
        return entity

    def system(
        self,
        *required_components: ComponentKey,
        pipeline: SystemsPipeline | None = None,
    ) -> t.Callable[[SystemExecutor], None]:
        """Add a system to the scene.

        This method returns a decorator function that takes a
        system executor callable as an argument.

        System executor signature must be::

            (Application, set[Entity]) -> None

        Function system executor example::

            scene = Scene("my scene")

            @scene.system(ComponentA, ComponentB, ...)
            def movement_system(app: Application, entities: set[Entity]) -> None:
                ...  # system code here

            ### or

            def movement_system(app: Application, entities: set[Entity]) -> None:
                ...  # system code here

            scene.system(ComponentA, ComponentB, ...)(movement_system)

        Callable object system executor example::

            scene = Scene("my scene")

            class System:

                def __call__(app: Application, entities: set[Entity]) -> None:
                    ...  # system code here

            scene.system(ComponentA, ComponentB, ...)(System())

        :param ComponentKey required_components: A list of components required
            by the system.
        :param SystemsPipeline | None pipeline: A pipeline to which to add the
            system, defaults to None

        :return t.Callable[[SystemExecutor], None]: A decorator function that registers the system.
        """

        def decorator(executor: SystemExecutor) -> None:
            system = make_system(executor, self._ec_table, *required_components)
            if pipeline is not None:
                pipeline.add(system)
            else:
                self._systems_schedule.update.add(system)

        return decorator

    def start(self) -> None:
        """Do a scene statup.

        This method is called before the fisrt game loop iteration.
        """
        self.logger.info(f"Starting up {repr(self.name)} scene...")
        for pipeline in (self._systems_schedule.start, self._systems_schedule.update):
            for system in pipeline._systems:
                system.update_entities()
        self._systems_schedule.start.run(self._app)

    def update(self) -> None:
        """Update scene.

        This method runs update systems.
        """
        self._systems_schedule.update.run(self._app)

    def finish(self) -> None:
        """Do a scene cleanup.

        This method is called after a last frame
        before scene switch or application shutdown.
        """
        self.logger.info(f"Cleaning up '{self.name}' scene...")
