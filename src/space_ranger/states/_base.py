from abc import ABC, abstractmethod

import pygame

from space_ranger.logging import LoggerMixin

StateId = str


class State(ABC, LoggerMixin):
    """An application state."""

    def __init__(self, state_id: StateId) -> None:
        self._id = state_id
        self._done = False
        self._quit = False
        self._previous: StateId | None = None

    @property
    def id(self) -> StateId:  # noqa: A003
        """A state id."""
        return self._id

    @property
    def done(self) -> bool:
        """A flag indicating whether a state is finished."""
        return self._done

    @property
    def quit(self) -> bool:  # noqa: A003
        """A flag indicating whether an app shoud be stopped."""
        return self._quit

    @property
    def previous(self) -> StateId | None:
        """A previous state id."""
        return self._previous

    @previous.setter
    def previous(self, value: StateId) -> None:
        assert isinstance(value, StateId)
        self._previous = value

    def startup(self) -> None:  # noqa: B027
        """Do a state statup."""
        self.logger.info(f"Starting up {self.__class__.__name__} state...")

    def cleanup(self) -> None:
        """Do a state cleanup."""
        self.logger.info(f"Cleaning up {self.__class__.__name__} state...")
        self._done = False

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update state.

        :param float delta_time: Delta time.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw state on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        raise NotImplementedError()

    def get_next(self) -> StateId:
        """Get a next state id."""
        return ""
