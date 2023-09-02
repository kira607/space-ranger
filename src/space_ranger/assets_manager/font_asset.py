from pathlib import Path
from typing import Any

import pygame

from space_ranger.assets_manager.asset import Asset


class FontFactory:
    """A font factory.

    Can load fonts and create new pygame.font.Font instances.

    :param str | Path | None path: A path to the font file.
    """

    def __init__(self, path: str | Path | None, **kwargs: Any) -> None:
        self.path = path
        self.kwargs = kwargs

    def __call__(self, size: int) -> pygame.font.Font:
        """Load font using given size."""
        return pygame.font.Font(self.path, size=size, **self.kwargs)


class FontAsset(Asset[FontFactory]):
    """A font asset."""

    sub_dir = "fonts"

    def load_asset(self) -> None:
        """Load font asset."""
        self.asset = FontFactory(self.path, **self.kwargs)
