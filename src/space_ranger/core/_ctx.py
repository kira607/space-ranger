import os
from pathlib import Path

import pygame as pg


class Controls:
    """Game controls."""

    move_up: int = pg.K_w
    move_left: int = pg.K_a
    move_down: int = pg.K_s
    move_right: int = pg.K_d


class Screen:
    """Helper object that simplifies working with screen."""

    width: int = 640
    height: int = 480
    fps: int = 60
    vsync: int = 1

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


class Config:
    """Application configuration."""

    logging_level: str = "CRITICAL"
    debug: bool = False
    assets_dir: Path = None
    builtin_assets_dir: Path = Path(os.path.dirname(__file__), "builtin_assets")


class ApplicationContext:
    """An application context."""

    controls = Controls()
    screen = Screen()
    config = Config()

    _debug_text_font: pg.font.Font = None
    _debug_text_color: pg.color.Color = (0, 255, 0)
    _debug_text_background: pg.color.Color = pg.Color(20, 20, 20, 230)

    @classmethod
    @property
    def debug_text_font(cls) -> pg.font.Font:
        """Get a text font for debug labels."""
        if cls._debug_text_font is None:
            cls._debug_text_font = pg.font.Font(Path(cls.config.builtin_assets_dir, "fonts", "JetBrainsMono-Thin.ttf"))
        return cls._debug_text_font
    
    @classmethod
    @property
    def debug_text_color(cls) -> pg.Color:
        """Get a text color for debug labels."""
        return cls._debug_text_color
    
    @classmethod
    @property
    def debug_text_background(cls) -> pg.Color:
        """Get a text background color for debug labels."""
        return cls._debug_text_background


ctx = ApplicationContext
