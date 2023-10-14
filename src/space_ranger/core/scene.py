from __future__ import annotations

import pygame as pg

from .logging import LoggerMixin


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
        self._id = str(scene_id)
        self._done = False
        self._quit = False
        self._previous: str | None = None
        self._next: str | None = None

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

    def start(self) -> None:
        """Do a scene statup.

        This method is called before the fisrt game loop iteration.
        """
        self.logger.info(f"Starting up {self.__class__.__name__} ({repr(self.id)}) scene...")
        self._start()

    def process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        """
        self._process_event(event)

    def update(self, delta_time: int) -> None:
        """Update scene.

        :param int delta_time: Delta time (in milliseconds).
        """
        self._update(delta_time)

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

    def _process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        """
        pass

    def _update(self, delta_time: int) -> None:
        """Update scene.

        :param int delta_time: Delta time (in milliseconds).
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
