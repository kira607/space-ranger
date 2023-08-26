from pathlib import Path

import pygame

from space_ranger.assets_manager.asset import Asset


class _MusicPlayer:
    """A music player."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def set_volume(self, volume: float) -> None:
        """Set music volume.

        :param float volume: New volume value (between 0.0 and 1.0).
        """
        pygame.mixer.music.set_volume(volume)

    def play(self) -> None:
        """Start plaing music."""
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()

    def stop(self) -> None:
        """Stop playing music."""
        pygame.mixer.music.stop()


class MusicAsset(Asset[_MusicPlayer]):
    """A music asset."""

    sub_dir = "music"

    def load_asset(self) -> None:
        """Load font asset."""
        self.asset = _MusicPlayer(self.path)
