"""A main Space ranger package."""

from space_ranger.application import Application
from space_ranger.states import MainMenu


def create_app() -> Application:
    """Create an app."""
    # build context
    states = {state.id: state for state in (MainMenu("main_menu"),)}
    # initiaize globally available singleton
    # create app
    app = Application(states, "main_menu")
    return app
