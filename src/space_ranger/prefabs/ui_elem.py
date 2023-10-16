import pygame as pg

from space_ranger.core import GameObject
from space_ranger.core.property import Bool


class UIElem(GameObject):
    """UI element."""

    is_hovered = Bool()
    is_clicked = Bool()

    def process_event(self, event: pg.event.Event) -> None:
        """Process event..."""
        self.is_hovered = self.rect.collidepoint(*pg.mouse.get_pos())

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_clicked = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False

        # dragging could be implemented like this
        # if all((event.type == pg.MOUSEMOTION, self.is_clicked)):
        #     self.set_transform(self.x + event.rel[0], self.y + event.rel[1])

        super().process_event(event)
