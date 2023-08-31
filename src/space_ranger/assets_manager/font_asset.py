from pathlib import Path
from typing import Any

import pygame

from space_ranger.assets_manager.asset import Asset


class _Font:
    """A font asset."""

    def __init__(self, path: Path, **kwargs: Any) -> None:
        self.path = path
        self.kwargs = kwargs

    def __call__(self, size: int) -> pygame.font.Font:
        """Load font using given size."""
        return pygame.font.Font(self.path, size=size, **self.kwargs)


class FontAsset(Asset[_Font]):
    """A font asset."""

    sub_dir = "fonts"

    def load_asset(self) -> None:
        """Load font asset."""
        self.asset = _Font(self.path, **self.kwargs)
