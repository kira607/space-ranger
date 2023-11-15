from dataclasses import dataclass

import pygame as pg

from space_ranger.core import Resource


@dataclass(slots=True)
class Window(Resource):
    """A window powered by pygame."""

    _width: int = 0
    _height: int = 0
    _caption: str = "Window"
    _fullscreen: bool = False
    _vsync: bool = False

    def __post_init__(self) -> None:  # noqa: D105
        self._apply()

    @property
    def width(self) -> int:
        """Width of the window."""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = int(value)
        self._apply()

    @property
    def height(self) -> int:
        """Height of the window."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = int(value)
        self._apply()

    @property
    def size(self) -> pg.math.Vector2:
        """Get widnow size as a 2d vector."""
        return pg.math.Vector2(self._width, self._height)

    def set_size(self, width: int = 0, height: int = 0) -> None:
        """Set window size.

        :param int width: Width of the window, defaults to 0.
        :param int height: Height of the window, defaults to 0.
        """
        self._width = width
        self._height = height
        self._apply()

    @property
    def caption(self) -> str:
        """Get window caption.

        :return str: A window caption.
        """
        return self._caption

    def set_caption(self, caption: str) -> None:
        """Set window caption.

        :param str caption: A window caption.
        """
        pg.display.set_caption(caption)

    @property
    def fullscreen(self) -> bool:
        """Get fullscreen flag.

        :return bool: `True` if window is fullscreen, `False` otherwise.
        """
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        self._fullscreen = value
        self._apply()

    @property
    def vsync(self) -> bool:
        """Get vsync.

        :return bool: `True` if window vsync is enabled, `False` otherwise.
        """
        return self._vsync

    @vsync.setter
    def vsync(self, vsync: bool) -> None:
        self._vsync = vsync
        self._apply()

    @property
    def surface(self) -> pg.Surface:
        """Get active display surface."""
        return pg.display.get_surface()

    @property
    def center(self) -> pg.math.Vector2:
        """Get screen center point."""
        return pg.math.Vector2(self._width // 2, self._height // 2)

    def _apply(self) -> None:
        # prepare parameters
        size = (self._width, self._height)
        flags = 0 if not self._fullscreen else pg.FULLSCREEN
        depth = 0
        display = 0
        vsync = int(self._vsync)

        # update window
        pg.display.set_mode(
            size,
            flags,
            depth,
            display,
            vsync,
        )

        # make sure to have up-to-date display resolution
        self._width = self.surface.get_width()
        self._height = self.surface.get_height()
