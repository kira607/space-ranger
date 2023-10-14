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

    @classmethod
    def get_debug_font(cls) -> pg.font.Font:
        """Get a font for debug labels."""
        return pg.font.Font(Path(cls.config.builtin_assets_dir, "fonts", "JetBrainsMono-Thin.ttf"))


ctx = ApplicationContext
