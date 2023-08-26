import pygame

from space_ranger.assets_manager.asset import Asset


class SoundAsset(Asset[pygame.mixer.Sound]):
    """A sound asset."""

    sub_dir = "sounds"

    def load_asset(self) -> None:
        """Load sound asset."""
        self.asset = pygame.mixer.Sound(self.path)
