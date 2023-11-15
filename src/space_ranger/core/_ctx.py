from __future__ import annotations

import os
import typing as t
from dataclasses import dataclass
from pathlib import Path

import pygame as pg

from .logging import LoggerMixin


if t.TYPE_CHECKING:
    from .scene import Scene


class UnknownSceneIdError(Exception):
    """An exception raised when trying to switch to a scene with unknown id."""

    def __init__(self, scene_id: str) -> None:
        msg = f"Unknown scene id: {scene_id}."
        super().__init__(msg)


@dataclass(slots=True)
class Controls:
    """Game controls."""

    move_forward: int = pg.K_w
    move_left: int = pg.K_a
    move_backward: int = pg.K_s
    move_right: int = pg.K_d


@dataclass(slots=True)
class Screen:
    """Helper object that simplifies working with screen."""

    width: int = 640
    height: int = 480

    def init(self) -> None:
        """Initialize screen."""
        pg.display.set_mode()

    @property
    def size(self) -> pg.math.Vector2:
        """Get screen dimensions."""
        return pg.math.Vector2(self.width, self.height)

    @property
    def surface(self) -> pg.Surface:
        """Get active display surface."""
        return pg.display.get_surface()

    @property
    def center(self) -> pg.math.Vector2:
        """Get screen center point."""
        return pg.math.Vector2(self.width // 2, self.height // 2)


@dataclass(slots=True)
class Config:
    """Application configuration."""

    logging_level: str = "CRITICAL"
    debug: bool = False
    assets_dir: Path = None
    builtin_assets_dir: Path = Path(os.path.dirname(__file__), "builtin_assets")
    fps: int = 60
    vsync: int = 1
    fullscreen: bool = False


class DebugAssets:
    """Assets for debug labels."""

    def __init__(self) -> None:
        self._debug_text_font: pg.font.Font = None
        self._debug_text_color: pg.color.Color = (0, 255, 0)
        self._debug_text_background: pg.color.Color = pg.Color(20, 20, 20, 230)

    @property
    def debug_text_font(self) -> pg.font.Font:
        """Get a text font for debug labels."""
        if self._debug_text_font is None:
            self._debug_text_font = pg.font.Font(
                Path(self.config.builtin_assets_dir, "fonts", "JetBrainsMono-Thin.ttf"),
            )
        return self._debug_text_font

    @property
    def debug_text_color(self) -> pg.Color:
        """Get a text color for debug labels."""
        return self._debug_text_color

    @property
    def debug_text_background(self) -> pg.Color:
        """Get a text background color for debug labels."""
        return self._debug_text_background


class ApplicationContext(LoggerMixin):
    """An application context."""

    def __init__(self) -> None:
        self._screen = Screen()
        self._config = Config()

        self._title: str
        self.set_title("Application")

        self._delta_time: int = 0
        self._events: list[pg.event.Event] = []

        self._scenes: dict[str, Scene] = {}
        self._current_scene: Scene

        self._next_scene_id: str

    @property
    def screen(self) -> Screen:
        """Get screen."""
        return self._screen

    @property
    def config(self) -> Config:
        """Get application configuration."""
        return self._config

    @property
    def delta_time(self) -> int:
        """Get delta time.

        :return: Delta time (in milliseconds).
        :rtype: int
        """
        return self._delta_time

    @property
    def events(self) -> list[pg.event.Event]:
        """Get list of events.

        :return: List of events
        :rtype: list[pg.event.Event]
        """
        return self._events

    def set_title(self, title: str) -> None:
        """Set a title of the application.

        A title will be shown at the window title bar.

        :param title: A new application title.
        :type title: str
        """
        self._title = title
        pg.display.set_caption(self._title)

    def register_scene(self, scene: Scene) -> None:
        """Register a new scene.

        :param scene: A scene to register.
        :type scene: Scene
        """
        self._scenes[scene.name] = scene

    def get_current_scene(self) -> Scene:
        """Get a current scene.

        :return: Current scene
        :rtype: Scene
        """
        return self._current_scene

    def switch_scene(self, next_scene_id: str) -> None:
        """Switch a scene.

        :param next_scene_id: ID of a scene to switch to.
        :type next_scene_id: str

        :raises UnknownSceneIdError: Given `next_scene_id`
          doesn't match any known scene.
        """
        if (next_scene := self._scenes.get(next_scene_id)) is None:
            raise UnknownSceneIdError(next_scene_id)

        self._current_scene.finish()
        self._current_scene = next_scene
        self._current_scene.start()


ctx = ApplicationContext()
