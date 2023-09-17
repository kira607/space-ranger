import pygame as pg

from space_ranger.core import Scene
from space_ranger.core.scene import SceneId
from space_ranger.prefabs import Button


class Playground(Scene):
    """A main menu state."""

    def __init__(self, scene_id: SceneId) -> None:
        super().__init__(scene_id)
        self.text = self.add_game_object(Button(hover_color=(127, 255, 127)))
        self.text.transform.x = 200
        self.text.transform.y = 200

    def draw(self, screen: pg.Surface) -> None:
        """Draw scene on a given screen.

        :param pg.Surface screen: Target screen.
        """
        screen.fill(pg.Color(230, 230, 230, 200))
        super().draw(screen)
