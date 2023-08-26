from typing import Mapping

import pygame

from space_ranger.logging import init_logging
from space_ranger.settings import Settings
from space_ranger.states import State, StateId


class Application:
    """A main application class.

    :param Settings settings: A settings object.
    :param dict[str, State] states: Application states collection.
    :param str initial_state_id: Id of an initial state.
    """

    def __init__(
        self,
        settings: Settings,
        states: Mapping[StateId, State],
        initial_state_id: str,
    ) -> None:
        self._settings = settings
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
        pygame.init()
        self._screen = pygame.display.set_mode(
            self._settings.size,
            pygame.HWSURFACE | pygame.DOUBLEBUF,
            vsync=self._settings.vsync,
        )
        self._clock = pygame.time.Clock()
        self._current_state.startup()
        self._running = True

    def _main_loop(self) -> None:
        """Run a main loop of the application."""
        while self._running:
            delta_time = self._clock.tick(self._settings.fps) / 1000.0
            self._process_events()
            self._update(delta_time)
            self._render()

    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            self._current_state.process_event(event)

    def _update(self, delta_time: float) -> None:
        """Run current state update.

        :param float delta_time: Delta time.
        """
        if self._current_state.quit:
            self._running = False
        elif self._current_state.done:
            self._current_state = self._get_next_state()
        self._current_state.update(self._screen, delta_time)

    def _render(self) -> None:
        """Render current state."""
        pygame.display.flip()

    def _cleanup(self) -> None:
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
