from dataclasses import fields

import pygame as pg

from space_ranger.core import ctx
from space_ranger.core.component import ComponentKey, Debug, Sprite
from space_ranger.core.entity import Entity
from space_ranger.core.utils import get_text_surface

from ._system import System


"""
+ EditorContainer (scrollable) (~20% of screen, on right side)
+-+ EntityContainer
+-+-+ Entity Title | Entity ID
+-+-+ ComponentContainer (1)
+-+-+-+ Property name | Property value editor (Text input, Number input, slider, checkbox, etc.)
+-+-+-+ ...
+-+-+ ComponentContainer (2)
+-+-+-+ ...
+-+ EntityContainer
+-+-+ Entity Title | Entity ID
+-+-+ ComponentContainer (1)
+-+-+-+ ...
+-+-+-+ ...
+-+-+ ComponentContainer (2)
+-+-+-+ ...
"""

class EditorCanvas:
    def __init__(self, screen: pg.Surface):
        self.screen = screen



class DebugSystem(System):
    """A system for debug editor."""

    def __init__(self, group: int = 0) -> None:
        super().__init__(group)
        self.editor_canvas = None
        self.prev = 0

    def _match_entity(self, entity: Entity) -> set[ComponentKey]:
        return entity.components.keys()


@DebugSystem.before_start
def _before_start(self: DebugSystem) -> None:
    self.editor_canvas = EditorCanvas(ctx.screen.surface)


@DebugSystem.start_entity
def _start_entity(self: DebugSystem, entity_id: int) -> None:
    # self.queued_entities[entity_id][Debug] = Debug()
    pass


@DebugSystem.update_entity
def _update_entity(self: DebugSystem, entity_id: int, events: list[pg.event.Event], delta_time: int) -> None:
    screen = ctx.screen.surface
    prev = 0
    for component in self.queued_entities[entity_id].values():
        if component.get_key() == Sprite:
            pg.draw.rect(screen, "red", component.rect, width=1)
        title = str(component.get_key())
        lines = [
            f"{field.name}: {str(getattr(component, field.name))[:300]}" for field in fields(component)
        ]
        s = get_text_surface(
            title,
            *lines,
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
            alignment="right",
        )
        pos = (ctx.screen.width - s.get_width(), prev)
        screen.blit(s, pos)
        prev += s.get_height()


@DebugSystem.after_update
def _after_update(self: DebugSystem, events: list[pg.event.Event], delta_time: int) -> None:
    self.prev = 0
