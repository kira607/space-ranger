from dataclasses import dataclass


@dataclass
class Settings:
    """A settings class."""

    fps: int = 60
    width: int = 640
    height: int = 480
    vsync: int = 0

    @property
    def size(self) -> tuple[int, int]:
        """Get window size."""
        return self.width, self.height
