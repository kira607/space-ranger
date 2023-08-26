import pygame

from space_ranger.assets_manager.asset import Asset


class ImageAsset(Asset[pygame.Surface]):
    """An image asset."""

    sub_dir = "images"

    def load_asset(self) -> None:
        """Load image asset."""
        self.asset = pygame.image.load(self.path, **self.kwargs)
