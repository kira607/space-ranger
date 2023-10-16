from __future__ import annotations

import abc
import typing as t

import pygame as pg

from .logging import LoggerMixin
from .property import PropertiesObserver


if t.TYPE_CHECKING:
    from .scene import Scene


class GameObject(PropertiesObserver, pg.sprite.Sprite, LoggerMixin, abc.ABC):
    """A base game object."""

    __enabled__ = False
    _name: str | None = None
    _scene: Scene | None

    def __new__(cls: type[GameObject], *args: t.Any, **kwargs: t.Any) -> GameObject:  # noqa: D102
        # dirty hack to prevent writing super().__init__() in each game object. (yes im lazy)
        obj = super().__new__(cls)
        obj.__enabled__ = False
        obj._name = None
        obj._scene = None
        super(cls, obj).__init__()
        return obj

    @property
    def scene(self) -> Scene | None:
        """Get a scene instance containing this game object."""
        return self._scene

    @property
    def is_enabled(self) -> bool:
        """Get if the GameObject is enabled.

        :return: Whether the GameObject is enabled.
        :rtype: bool
        """
        return self.__enabled__

    def enable(self) -> None:
        """Enable the GameObject.

        If an object is already enabled does nothing.

        When a GameObject is enabled:
        - The GameObject is updated each frame.
        - All animations are applied to the GameObject.
        - The GameObject is drawn on a screen.
        """
        self.__enabled__ = True

    def disable(self) -> None:
        """Disable the GameObject.

        If an object is already disabled does nothing.

        When a GameObject is disabled:
        - The GameObject is not updated.
        - No animations are applied to the GameObject.
        - The GameObject is not drawn on a screen.
        """
        self.__enabled__ = False

    def set_layer(self, layer: int) -> None:
        """Set object layer.

        High layer objects are drawn later on the screen.

        :param layer: The layer.
        :type layer: int
        """
        self._layer = layer
        return self

    def build(self) -> None:
        """Build game object."""
        if not self.is_enabled:
            # There is no point in building disabled game object.
            return
        self._build()
        self.rect = self.image.get_rect()

    def start(self) -> None:
        """Start game object.

        This method is called before a first frame.
        """
        self.logger.debug(f"{self.scene.id} | Building {self._name}...")
        self.enable()
        self.build()
        self._start()

    def process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param event: pygame event.
        :type event: pygame.event.Event
        """
        self._process_event(event)

    def update(self, delta_time: int) -> None:
        """Update game object.

        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        self._update(delta_time)

    def _build(self) -> None:
        """Build game object.

        In most cases for single sprites this method
        can be overridden to assign
        a pygame surface to `self.image`.
        """
        pass

    def _start(self) -> None:
        """Start game object.

        This method is called before a first frame.
        """
        pass

    def _process_event(self, event: pg.event.Event) -> None:
        """Process a pygame event.

        :param event: pygame event.
        :type event: pygame.event.Event
        """
        pass

    def _update(self, delta_time: int) -> None:
        """Update game object.

        :param delta_time: Delta time (in milliseconds).
        :type delta_time: int
        """
        pass

    def __bool__(self) -> bool:
        """Get a bool value of the GameObject.

        The GameObject is True if it is enabled, False otherwise.
        """
        return self.__enabled__
