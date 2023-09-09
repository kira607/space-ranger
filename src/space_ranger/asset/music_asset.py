from pathlib import Path

import pygame as pg

from .asset import Asset


class MusicPlayer:
    """A music player."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def set_volume(self, volume: float) -> None:
        """Set music volume.

        :param float volume: New volume value (between 0.0 and 1.0).
        """
        pg.mixer.music.set_volume(volume)

    def play(self) -> None:
        """Start plaing music."""
        pg.mixer.music.unload()
        pg.mixer.music.load(self.path)
        pg.mixer.music.play()

    def stop(self) -> None:
        """Stop playing music."""
        pg.mixer.music.stop()


class MusicAsset(Asset[MusicPlayer]):
    """A music asset."""

    sub_dir = "music"

    def _load_asset(self) -> MusicPlayer:
        """Load music asset."""
        return MusicPlayer(self.path)
