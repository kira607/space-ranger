from __future__ import annotations

import abc
import typing as t

import pygame as pg

from space_ranger.logging import LoggerMixin

from .common import HasProperties, Observer
from .component import Component, Transform, isdrawable
from .property import Property

if t.TYPE_CHECKING:
    from .scene import Scene

__all__ = ["GameObject"]


class GameObject(Observer, HasProperties, LoggerMixin, abc.ABC):
    """A base game object.

    A game object is an observer of its properties and components.

    When a Property or a Component is chaged it notifies
    its GameObject which triggers a GameObject.accept_notification().
    """

    __enabled__ = True

    __drawables__: pg.sprite.LayeredUpdates
    __components__: list[Component]
    __children__: list[GameObject]

    __parent__: GameObject | None
    __scene__: Scene | None

    transform: Transform

    def __new__(cls: type[GameObject], *args: t.Any, **kwargs: t.Any) -> GameObject:
        obj = super().__new__(cls)
        obj.__drawables__ = pg.sprite.LayeredUpdates()
        obj.__components__ = []
        obj.__children__ = []
        obj.__parent__ = None
        obj.__scene__ = None
        obj.transform = obj.add_component(Transform())
        return obj

    def add_child(self, child: GameObject) -> GameObject:
        self.__children__.append(child)
        child.__parent__ = self
        return child

    def add_component(self, component: Component, layer: int = 0) -> Component:
        self.__components__.append(component)
        if isdrawable(component):
            self.__drawables__.add(component, layer=layer)
        component.game_object = self
        return component

    def start(self):
        self.build()

    def build(self) -> None:
        """Build game object."""
        # reposition drawables
        for drawable in self.__drawables__:
            drawable.build()
            pg.transform.rotate(drawable.image, self.transform.r)
            drawable.rect = drawable.image.get_rect()
            drawable.rect.center = self.transform.x, self.transform.y
        # reposition children
        for child in self.__children__:
            child.transform = self.transform + child.transform

    def process_event(self, event):
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
        self.__drawables__.draw(screen)

        # draw child game objects
        for child in self.__children__:
            child.draw(screen)

    def accept_notification(self) -> None:
        """Accept a notification from a component or property."""
        self.build()

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


class NewGameObject(Observer, HasProperties, pg.sprite.Sprite, LoggerMixin, abc.ABC):
    __enabled__ = True

    __children__: list[GameObject]
    __parent__: GameObject | None
    __scene__: Scene | None

    transform = Transform()

    def __new__(cls: type[NewGameObject], *args: t.Any, **kwargs: t.Any) -> NewGameObject:
        obj = super().__new__(cls)
        obj.__children__ = []
        obj.__parent__ = None
        obj.__scene__ = None
        return obj

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
