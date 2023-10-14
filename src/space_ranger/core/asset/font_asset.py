from pathlib import Path
from typing import Any

import pygame as pg

from .asset import Asset


class FontFactory:
    """A font factory.

    Can load fonts and create new pygame.font.Font instances.

    :param str | Path | None path: A path to the font file.
    """

    def __init__(self, path: str | Path | None, **kwargs: Any) -> None:
        self.path = path
        self.kwargs = kwargs

    def __call__(self, size: int = 16) -> pg.font.Font:
        """Load font using given size."""
        return pg.font.Font(self.path, size=size, **self.kwargs)


class FontAsset(Asset[FontFactory]):
    """A font asset."""

    sub_dir = "fonts"

    def _load_asset(self) -> FontFactory:
        """Load font asset."""
        return FontFactory(self.path, **self._kwargs)
