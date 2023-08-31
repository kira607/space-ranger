from dataclasses import dataclass


@dataclass
class Settings:
    """A settings class."""

    screen_width: int = 0
    screen_height: int = 0
    fps: int = 60
    vsync: int = 0

    @property
    def screen_size(self) -> tuple[int, int]:
        """Get window size."""
        return self.screen_width, self.screen_height
