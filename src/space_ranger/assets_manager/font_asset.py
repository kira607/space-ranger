import pygame

from space_ranger.assets_manager.asset import Asset


class FontAsset(Asset[pygame.font.Font]):
    """A font asset."""

    sub_dir = "fonts"

    def load_asset(self) -> None:
        """Load font asset."""
        self.asset = pygame.font.Font(self.path, **self.kwargs)
