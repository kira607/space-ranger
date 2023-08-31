"""A main Space ranger package."""

from .app import create_app as create_app

__all__ = ["create_app", "current_app"]
__version__ = "0.1"
