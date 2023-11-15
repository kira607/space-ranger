from __future__ import annotations

import typing as t
import uuid
from dataclasses import dataclass, field
from enum import Enum

from .component import ComponentKey
from .entity import Entity, EntityUid
from .errors import SystemExecutorIsNotCallableError


if t.TYPE_CHECKING:
    from .application import Application
    from .ec_table import EcTable


type SystemExecutor = t.Callable[[Application, set[Entity]], None]


class System:
    """Base system.

    A :class:`System` is a wrapper over system executor.

    A system executor is any callable object that operates
    over entities.

    Each system has a set of required components
    which is used to query entities from :class:`EcTable`.

    :param str name: The name of the system.
    :param SystemExecutor executor: A system executor.
        Can be any callable object that matches :ref:`SystemExecutor` signature.
    :param EcTable ec_table: The EcTable instance over which the system
        will be working on.
    :param Component required_components: A list of components keys
        required by this system.
    """

    def __init__(
        self,
        name: str,
        executor: SystemExecutor,
        ec_table: EcTable,
        *required_components: ComponentKey,
    ) -> None:
        self._name = name
        self._executor = executor
        self._ec_table = ec_table
        self._required_components = set(required_components)
        self._entities: set[EntityUid] = set()

    def match_entity(self, entity_uid: EntityUid) -> bool:
        """Check if an entity matches this system by its components.

        Entity matches a system when it has all the components
        that are required by a system. Entity can have more components
        than required ones, but never less.

        If required components set is empty any entity
        will match this system.

        :param EntityUid entity_uid: UID of an entity to check for compatibility.

        :return bool: `True`, if the entity matches this system, `False` otherwise.
        """
        return all(
            self._ec_table.get_component(entity_uid, component_key) is not None
            for component_key in self._required_components
        )

    def add_entity(self, entity_uid: EntityUid) -> None:
        """Add an entity to the system processing queue.

        :param EntityUid entity_uid: UID of entity to add for processing.
        """
        self._entities.add(entity_uid)

    def remove_entity(self, entity_uid: EntityUid) -> None:
        """Remove an entity from the system processing queue.

        :param EntityUid entity_uid: UID of entity to remove from processing.
        """
        self._entities.remove(entity_uid)

    def update_entities(self) -> None:
        """Update entities processing queue.

        Queries :class:`EcTable` for compatible entities and
        updates processing queue.
        """
        self._entities = {entity.uid for entity in self._ec_table.iter_entities() if self.match_entity(entity.uid)}

    def run(self, app: Application) -> None:
        """Run a system."""
        self._executor(app, {self._ec_table.get_entity_by_uid(uid) for uid in self._entities})


def make_system(system_executor: SystemExecutor, ec_table: EcTable, *required_components: ComponentKey) -> System:
    """Create a system out of system executor.

    System executor may be any callable,
    whether it's a function or a callable class,
    that matches a :ref:`SystemExecutor` signature.

    Function system executor example:

        .. code-block:: python

        def movement_system(app: Application, entities: set[Entity]) -> None:
            ...  # system code here

        make_system(movement_system, ec_table, ComponentA, ComponentB, ...)

    Callable object system executor example::

        class MovementSystem:
            def __call__(self, app: Application, entities: set[Entity]) -> None:
                ...  # system code here

        make_system(MovementSystem(), ec_table, ComponentA, ComponentB, ...)

    ...  # For some reason vscode ignores this line when showing function docsting on hover?
    A name of a system is determined by executor type:
    * If it is a function a function name is taken.
    * If it is a class a class name is taken.
    * In any other case a name is generated using uuid (System-{uuid4()})

    :param SystemExecutor system_executor: A system executor.
        Can be any callable object that matches :ref:`SystemExecutor` signature.
    :param EcTable ec_table: The EcTable instance over which the system
        will be working on.
    :param Component required_components: A list of components keys
        required by this system.

    :raises SystemExecutorIsNotCallableError: A given system executor is not
        a callable object.

    :return System: A system instance.
    """
    if not callable(system_executor):
        raise SystemExecutorIsNotCallableError(system_executor)

    # pick a name for the system
    if hasattr(system_executor, "__name__"):
        name = system_executor.__name__
    elif hasattr(system_executor, "__class__"):
        name = system_executor.__class__.__name__
    else:
        name = f"System-{uuid.uuid4()}"

    system = System(name, system_executor, ec_table, *required_components)
    return system


class SystemsPipeline:
    """Systems pipeline.

    A pipeline contains a set of :class:`System` instances
    and is used inside a :class:`SystemsSchedule` to manage
    the order of systems execution.
    """

    def __init__(self) -> None:
        self._systems: set[System] = set()

    def add(self, system: System) -> None:
        """Add a system to the pipeline.

        :param System system: A system to be added to the pipeline.
        """
        self._systems.add(system)

    def run(self, app: Application) -> None:
        """Run a pipeline.

        :param Application app: An application in which this pipeline is working.
        """
        for system in self._systems:
            system.run(app)


@dataclass(slots=True, frozen=True)
class SystemsSchedule:
    """Systems schedule.

    A schedule contains a set of :class:`SystemsPipeline`
    organized in a particular order.
    """

    # Generally, there are two groups of pipelines: startup and update.
    # Startup pipelines run before the first frame of the application.
    # They also can be called for a newly instantiated entity.
    # Update pipelines run each frame.

    start: SystemsPipeline = field(default_factory=SystemsPipeline)
    update: SystemsPipeline = field(default_factory=SystemsPipeline)
