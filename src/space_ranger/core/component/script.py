from __future__ import annotations

from dataclasses import dataclass

import pygame as pg

from ._component import Component


@dataclass(slots=True)
class Script(Component):
    """Script component."""

    def start(self) -> None:
        """Start component."""
        self._start()

    def update(self, events: list[pg.event.Event], delta_time: int) -> None:
        """Update component.

        :param events: List of pygame events to process.
        :type events: list[pg.event.Event]
        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        self._update(events, delta_time)

    def _start(self) -> None:
        """Run start hook.

        This method is called before the first frame.
        """
        pass

    def _update(self, events: list[pg.event.Event], delta_time: int) -> None:
        """Run update hook.

        This method is called every frame.

        :param events: List of pygame events to process.
        :type events: list[pg.event.Event]
        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        pass
