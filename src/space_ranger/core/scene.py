from __future__ import annotations

import abc
import inspect
import typing as t

import pygame as pg

from space_ranger.logging import LoggerMixin

from .game_object import GameObject
from .properties_observer import PropertiesObserver
from .property import Color

SceneId = str


# TODO: forbid scenes inheritance deeper than 1
class Scene(PropertiesObserver, LoggerMixin, abc.ABC):
    """An application scene.

    Scene consists of game objects.
    """

    _game_objects: list[GameObject]

    background_color = Color(255)

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> Scene:  # noqa: D102
        obj = super().__new__(cls)
        obj._game_objects = []
        for _, go in inspect.getmembers(obj.__class__, lambda p: isinstance(p, GameObject)):
            obj.add_game_object(go)
            go._name = _
        return obj

    def __init__(self, scene_id: SceneId) -> None:
        self._id = scene_id
        self._done = False
        self._quit = False
        self._previous: SceneId | None = None

    def add_game_object(self, game_object: GameObject) -> GameObject:
        """Add a game object to a scene.

        :param game_object: A game object to add to the scene.
        :type game_object: GameObject

        :return: The game object added.
        :rtype: GameObject
        """
        self._game_objects.append(game_object)
        game_object._scene = self
        return game_object

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
        """Do a scene statup.

        This method is called before the fisrt game loop iteration.
        """
        self.logger.info(f"Starting up {self.__class__.__name__} ({repr(self.id)}) scene...")
        self.logger.info(f"{self.__class__.__name__} ({repr(self.id)}) | Game objects: {len(self._game_objects)}")
        for game_object in self._game_objects:
            game_object.start()
        self._start()

    def _start(self) -> None:
        """User defined start function.

        At this point all scene game objects are built.
        """
        pass

    def finish(self) -> None:
        """Do a scene cleanup."""
        self.logger.info(f"Cleaning up {self.__class__.__name__} scene...")
        self._done = False

    def process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        """
        for obj in self._game_objects:
            if obj.is_enabled:
                obj.process_event(event)

    def update(self, delta_time: int) -> None:
        """Update scene.

        :param int delta_time: Delta time (in milliseconds).
        """
        for obj in self._game_objects:
            if obj.is_enabled:
                obj.update(delta_time)

    def draw(self, screen: pg.Surface) -> None:
        """Draw scene on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.fill(self.background_color)
        for obj in self._game_objects:
            if obj.is_enabled:
                obj.draw(screen)

    def get_next(self) -> SceneId:
        """Get a next scene id."""
        return ""

    def _accept_notification(self) -> None:
        pass
