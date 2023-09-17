from __future__ import annotations

import abc
import typing as t

import pygame as pg

from space_ranger.logging import LoggerMixin

from .properties_observer import PropertiesObserver
from .property import Angle, Float

if t.TYPE_CHECKING:
    from .scene import Scene


class Transform(PropertiesObserver):
    """Game object transform."""

    x = Float()
    y = Float()
    r = Angle()

    game_object: GameObject

    @classmethod
    def from_vector(cls, vector: pg.Vector3) -> Transform:
        """Create a new Transform from `pygame.Vector3`."""
        return cls(vector.x, vector.y, vector.z)

    @property
    def vector(self) -> pg.Vector3:
        """Get transform as a vector."""
        return pg.Vector3(self.x, self.y, self.r)

    def __add__(self, other: Transform) -> Transform:
        """Add two trasform objects."""
        return Transform.from_vector(self.vector + other.vector)

    def _accept_notification(self) -> None:
        self.game_object._accept_notification()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.game_object}, [{self.x}, {self.y}, {self.r}])"


class GameObject(PropertiesObserver, pg.sprite.Sprite, LoggerMixin, abc.ABC):
    """A base game object.

    A game object is an observer of its properties and components.

    When a Property or a Component is chaged it notifies
    its GameObject which triggers a GameObject.accept_notification().
    """

    __enabled__ = True

    __children__: list[GameObject]
    __parent__: GameObject | None
    __scene__: Scene | None

    transform: Transform

    def __new__(cls: type[GameObject], *args: t.Any, **kwargs: t.Any) -> GameObject:
        obj = super().__new__(cls)
        obj.__children__ = []
        obj.__parent__ = None
        obj.__scene__ = None
        obj.transform = Transform()
        obj.transform.game_object = obj
        return obj

    def start(self) -> None:
        """Start game object."""
        self.build()

    def build(self) -> None:
        """Build game object."""
        self._build()
        self.image = pg.transform.rotate(self.image, self.transform.r)
        self.rect = self.image.get_rect()
        self.rect.center = self.transform.x, self.transform.y
        # reposition children
        for child in self.__children__:
            child.transform = self.transform + child.transform

    @abc.abstractmethod
    def _build(self) -> None:
        raise NotImplementedError()

    def process_event(self, event: pg.event.Event) -> None:
        """Process pygame event."""
        pass

    def update(self, delta_time: int) -> None:
        """Update game object."""
        # play animations
        pass

    def draw(self, screen: pg.Surface) -> None:
        """Draw a game object on a screen.

        :param pg.Surface screen: Target screen.
        """
        # draw drawable components
        screen.blit(self.image, self.rect)

        # draw child game objects
        for child in self.__children__:
            child.draw(screen)

    def _accept_notification(self) -> None:
        """Accept a notification from a component or property."""
        self.build()

    def add_child(self, child: GameObject) -> GameObject:
        self.__children__.append(child)
        child.__parent__ = self
        return child

    @property
    def is_enabled(self) -> bool:
        """Get if the GameObject is enabled.

        :return: Whether the GameObject is enabled.
        :rtype: bool
        """
        return bool(self)

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

    def __bool__(self) -> bool:
        """Get a bool value of the GameObject.

        The GameObject is True if it is enabled, False otherwise.
        """
        return self.__enabled__
