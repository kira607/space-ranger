import pygame

from .asset import Asset


class ImageAsset(Asset[pygame.Surface]):
    """An image asset."""

    sub_dir = "images"

    def _load_asset(self) -> pygame.Surface:
        """Load image asset."""
        return pygame.image.load(self.path, **self._kwargs).convert_alpha()
