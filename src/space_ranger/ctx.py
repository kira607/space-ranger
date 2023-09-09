import os
from pathlib import Path

import pygame as pg


class Controls:
    """Game controls."""

    move_up = pg.K_w
    move_left = pg.K_a
    move_down = pg.K_s
    move_right = pg.K_d


class Settings:
    """A settings class."""

    screen_width: int = 640
    screen_height: int = 480
    fps: int = 60
    vsync: int = 0

    @property
    def screen_size(self) -> tuple[int, int]:
        """Get window size."""
        return self.screen_width, self.screen_height


class Config:
    """Application configuration."""

    logging_level: str = "CRITICAL"
    assets_dir = Path(os.path.dirname(__file__), "assets")


class ApplicationContext:
    """An application context."""

    controls = Controls()
    settings = Settings()
    config = Config()
