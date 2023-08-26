"""A main Space ranger package."""

from space_ranger.app import App
from space_ranger.settings import Settings
from space_ranger.states import MainMenu

__all__ = ["create_app"]
__version__ = "0.1"


def create_app() -> App:
    """Create an app."""
    settings = Settings()
    states = {state.id: state for state in (MainMenu(),)}
    app = App(settings, states, "main_menu")
    return app
