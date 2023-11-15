from __future__ import annotations

import pygame as pg

from .entity import Entity
from .errors import UnknownSceneIdError
from .logging import LoggerMixin, init_logging
from .resource import Resource, ResourceKey
from .scene import Scene


# from .utils import get_text_surface


_DEFAULT_SCENE = Scene("__default__")


@_DEFAULT_SCENE.system(pipeline=_DEFAULT_SCENE._systems_schedule.start)
def _window_setup(app: Application, entities: set[Entity]) -> None:
    app.window.set_size(640, 480)


@_DEFAULT_SCENE.system()
def _close_window_on_esc(app: Application, entities: set[Entity]) -> None:
    for event in app.events:
        if event.type == pg.QUIT:
            app.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            app.quit()


class Application(LoggerMixin):
    """A main application class.

    :param title: The title of the application, defaults to "Application".
    """

    def __init__(self, title: str = "Application") -> None:
        init_logging()
        self.logger.info(f"Initializing application '{title}'...")

        self._resources: dict[ResourceKey, Resource] = {}
        self._title: str = title
        self._fps: int = 60
        self._delta_time: float = 0
        self._events: dict[int, pg.event.Event] = {}
        self._clock = pg.time.Clock()
        self._scenes: dict[str, Scene] = {}
        self._current_scene: Scene

        # initialize pygame
        pg.init()

        self.set_title(title)

    @property
    def current_scene(self) -> Scene:
        """Get the current scene."""
        return self._current_scene

    def switch_scene(self, next_scene_id: str) -> None:
        """Switch a scene.

        :param str next_scene_id: ID of a scene to switch to.

        :raises UnknownSceneIdError: Given `next_scene_id`
          doesn't match any known scene ID.
        """
        if (next_scene := self._scenes.get(next_scene_id)) is None:
            raise UnknownSceneIdError(next_scene_id)

        self._current_scene.finish()
        self._current_scene = next_scene
        self._current_scene.start()

    @property
    def delta_time(self) -> float:
        """Get frame delta time."""
        return self._delta_time

    @property
    def events(self) -> dict[int, pg.event.Event]:
        """Get a list of events."""
        return self._events

    @property
    def title(self) -> str:
        """Get application titile.

        :return str: An application title.
        """
        return self._title

    def set_title(self, title: str) -> None:
        """Set application titile.

        :param str title: An application titile.
        """
        self._title = str(title)

    def register_scene(self, scene: Scene) -> None:
        """Register a scene in the application.

        :param Scene scene: The scene to register.
        """
        self._scenes[scene.name] = scene
        scene._app = self

    def quit(self) -> None:  # noqa: A003
        """Quit the application."""
        self._running = False

    def run(self, start_scene_id: str = "__default__") -> None:
        """Run application.

        :param str start_scene_id: A starting scene id.
        """
        try:
            self._run(start_scene_id)
        except (Exception, KeyboardInterrupt) as e:
            self.logger.exception(f"Unhandled exception {e}:")
            self.logger.critical("Application has stopped because of an unhandled exception")
        finally:
            self._finish()

    def _run(self, start_scene_id: str) -> None:
        """Run a main loop of the application."""
        self.logger.info("Running main loop of the application")
        self._start(start_scene_id)
        while self._running:
            self._delta_time = self._clock.tick(self._fps)
            self._events = {event.type: event for event in pg.event.get()}
            self._update()

    def _start(self, start_scene_id: str) -> None:
        """Initialize application."""
        if not self._scenes:
            # raise ValueError("Cannot start application with zero scenes.")
            self.register_scene(_DEFAULT_SCENE)
            self._current_scene = _DEFAULT_SCENE

        if start_scene_id not in self._scenes:
            raise UnknownSceneIdError(start_scene_id)

        self._current_scene = self._scenes[start_scene_id]
        self._current_scene.start()
        self._running = True

    def _update(self) -> None:
        """Run current scene update."""
        self.current_scene.update()

    def _finish(self) -> None:
        """Cleanup before quitting the application."""
        self._current_scene.finish()
        pg.quit()

    # def _draw_debug_info(self) -> None:
    #     debug_surface = get_text_surface(
    #         f"FPS: {round(self._clock.get_fps(), 2)}",
    #         f"Scene: {self._current_scene.name}",
    #         f"Screen size: {ctx.screen.width}:{ctx.screen.height}",
    #         font=ctx.debug_text_font,
    #         color=ctx.debug_text_color,
    #         background=ctx.debug_text_background,
    #         antialias=True,
    #     )
    #     self._window.blit(debug_surface, (0, 0))

    #     # screen grid
    #     pg.draw.line(self._window, (30, 30, 30, 200), (0, ctx.screen.center.y), (ctx.screen.width, ctx.screen.center.y))
    #     pg.draw.line(
    #         self._window, (30, 30, 30, 200), (ctx.screen.center.x, 0), (ctx.screen.center.x, ctx.screen.height)
    #     )
