import pygame

from .asset import Asset


class SoundAsset(Asset[pygame.mixer.Sound]):
    """A sound asset."""

    sub_dir = "sounds"

    def _load_asset(self) -> pygame.mixer.Sound:
        """Load sound asset."""
        return pygame.mixer.Sound(self.path)
