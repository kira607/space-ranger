import pygame

StateId = str


class State:
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

    def startup(self) -> None:
        """Do a state statup."""
        pass

    def cleanup(self) -> None:
        """Do a state cleanup."""
        self._done = False

    def process_event(self, event: pygame.event.Event) -> None:
        """Process a pygame event.

        :param pygame.event.Event event: An event to process.
        :return: None
        """
        pass

    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """Update state.

        :param pygame.Surface screen: A current screen.
        :param float delta_time: Delta time.
        :return: None
        """
        pass

    def get_next(self) -> StateId:
        """Get a next state id."""
        return ""
