from __future__ import annotations

import abc

import pygame as pg

from space_ranger.logging import LoggerMixin

from .game_object import GameObject
from .has_children import HasChildren

SceneId = str


class Scene(HasChildren[GameObject], LoggerMixin, abc.ABC):
    """An application scene.

    Scene consists of game objects.
    """

    _child_node_type = GameObject

    def __init__(self, scene_id: SceneId) -> None:
        self._id = scene_id
        self._done = False
        self._quit = False
        self._previous: SceneId | None = None

    @property
    def id(self) -> SceneId:  # noqa: A003
        """A scene id."""
        return self._id

    @property
    def done(self) -> bool:
        """A flag indicating whether a scene is finished."""
        return self._done

    @property
    def quit(self) -> bool:  # noqa: A003
        """A flag indicating whether the app shoud be stopped."""
        return self._quit

    @property
    def previous(self) -> SceneId | None:
        """A previous scene id."""
        return self._previous

    @previous.setter
    def previous(self, value: SceneId) -> None:
        assert isinstance(value, SceneId)
        self._previous = value

    def start(self) -> None:
        """Do a scene statup."""
        self.logger.info(f"Starting up {self.__class__.__name__} scene...")
        for obj in self.__children__:
            self.logger.debug(f"{type(self).__name__} | Building {obj.name} ({type(obj).__name__})")
            obj.build()

    def finish(self) -> None:
        """Do a scene cleanup."""
        self.logger.info(f"Cleaning up {self.__class__.__name__} scene...")
        self._done = False

    def process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        """
        # TODO: how to process events?

    def update(self, delta_time: int) -> None:
        """Update scene.

        :param int delta_time: Delta time (in milliseconds).
        """
        for obj in self.__children__:
            if obj.is_enabled:
                obj.update(delta_time)

    def draw(self, screen: pg.Surface) -> None:
        """Draw scene on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        for obj in self.__children__:
            if obj.is_enabled:
                obj.draw(screen)

    def get_next(self) -> SceneId:
        """Get a next scene id."""
        return ""
