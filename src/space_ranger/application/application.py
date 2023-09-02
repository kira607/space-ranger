from typing import Mapping

import pygame

from space_ranger.globals import SETTINGS
from space_ranger.logging import LoggerMixin, init_logging
from space_ranger.states import State, StateId


class Application(LoggerMixin):
    """A main application class.

    :param Settings settings: A settings object.
    :param dict[str, State] states: Application states collection.
    :param str initial_state_id: Id of an initial state.
    """

    def __init__(
        self,
        states: Mapping[StateId, State],
        initial_state_id: str,
    ) -> None:
        self._states = states
        self._current_state = self._states[initial_state_id]
        self._running = False
        self._screen: pygame.Surface
        self._clock: pygame.time.Clock

    def run(self) -> None:
        """Run application."""
        self._init()
        self._main_loop()
        self._cleanup()

    def _init(self) -> None:
        """Initialize application."""
        init_logging()
        self.logger.info("Initializing application...")
        pygame.init()
        self._screen = pygame.display.set_mode(
            SETTINGS.screen_size,
            pygame.HWSURFACE | pygame.DOUBLEBUF,
            vsync=SETTINGS.vsync,
        )
        SETTINGS.screen_width = self._screen.get_width()
        SETTINGS.screen_height = self._screen.get_height()
        pygame.display.set_caption("Space Ranger")
        self._clock = pygame.time.Clock()
        self._current_state.startup()
        self._running = True

    def _main_loop(self) -> None:
        """Run a main loop of the application."""
        while self._running:
            delta_time = self._clock.tick(SETTINGS.fps)
            self._process_events()
            self._update(delta_time)
            self._draw()

    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            self._current_state.process_event(event)

    def _update(self, delta_time: int) -> None:
        """Run current state update.

        :param int delta_time: Delta time (in milliseconds).
        """
        if self._current_state.quit:
            self._running = False
        elif self._current_state.done:
            self._current_state = self._get_next_state()
        self._current_state.update(delta_time)

    def _draw(self) -> None:
        """Render current state."""
        self._current_state.draw(self._screen)
        pygame.display.flip()

    def _cleanup(self) -> None:
        """Cleanup before quitting application."""
        self._current_state.cleanup()
        pygame.quit()

    def _get_next_state(self) -> State:
        """Get a next state."""
        previous_state_id = self._current_state.id
        next_state_id = self._current_state.get_next()
        self._current_state.cleanup()
        next_state = self._states[next_state_id]
        next_state.previous = previous_state_id
        next_state.startup()
        return next_state
