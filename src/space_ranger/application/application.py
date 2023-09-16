from typing import Mapping

import pygame as pg

from space_ranger import ctx
from space_ranger.core import Scene, SceneId
from space_ranger.logging import LoggerMixin


class Application(LoggerMixin):
    """A main application class.

    :param Settings settings: A settings object.
    :param dict[str, State] states: Application states collection.
    :param str initial_state_id: Id of an initial state.
    """

    def __init__(
        self,
        scenes: Mapping[SceneId, Scene] | None = None,
        initial_scene_id: SceneId | None = None,
    ) -> None:
        self._scenes = scenes or {}
        self._current_scene = self._scenes[initial_scene_id] if scenes else None
        self._running = False
        self._screen: pg.Surface
        self._clock: pg.time.Clock

    def add_scene(self, scene_id, scene):
        self._scenes[scene_id] = scene

    def run(self, start_scene: SceneId) -> None:
        """Run application."""
        self._init(start_scene)
        self._main_loop()
        self._cleanup()

    def _init(self, start_scene: SceneId) -> None:
        """Initialize application."""
        self.logger.info("Initializing application...")
        if not self._scenes:
            raise ValueError("Cannot start application with zero scenes.")
        pg.init()
        self._screen = pg.display.set_mode(
            ctx.settings.screen_size,
            pg.HWSURFACE | pg.DOUBLEBUF,
            vsync=ctx.settings.vsync,
        )
        ctx.settings.screen_width = self._screen.get_width()
        ctx.settings.screen_height = self._screen.get_height()
        pg.display.set_caption("Space Ranger")
        self._clock = pg.time.Clock()
        self._current_scene = self._scenes[start_scene](start_scene)
        self._current_scene.start()
        self._running = True

    def _main_loop(self) -> None:
        """Run a main loop of the application."""
        self.logger.info("Running main loop of the application")
        while self._running:
            delta_time = self._clock.tick(ctx.settings.fps)
            self._process_events()
            self._update(delta_time)
            self._draw()

    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            self._current_scene.process_event(event)

    def _update(self, delta_time: int) -> None:
        """Run current state update.

        :param int delta_time: Delta time (in milliseconds).
        """
        if self._current_scene.quit:
            self._running = False
        elif self._current_scene.done:
            self._current_scene = self._get_next_scene()
        self._current_scene.update(delta_time)

    def _draw(self) -> None:
        """Render current state."""
        self._current_scene.draw(self._screen)
        pg.display.flip()

    def _cleanup(self) -> None:
        """Cleanup before quitting application."""
        self._current_scene.finish()
        pg.quit()

    def _get_next_scene(self) -> Scene:
        """Get a next state."""
        previous_state_id = self._current_scene.id
        next_state_id = self._current_scene.get_next()
        self._current_scene.finish()
        next_state = self._scenes[next_state_id]
        next_state.previous = previous_state_id
        next_state.start()
        return next_state
