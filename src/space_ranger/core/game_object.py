from __future__ import annotations

import abc
import typing as t

import pygame as pg

from space_ranger.core.has_children import HasChildren
from space_ranger.logging import LoggerMixin

from .has_children import HasChildren
from .property import Property

if t.TYPE_CHECKING:
    from .scene import Scene


class GameObject(HasChildren[Property], LoggerMixin, abc.ABC):
    """A base game object.

    A game object is an observer of its properties.

    When a GameObjectProperty is chaged it notifies
    its GameObject which triggers a GameObject.accept_notification().
    """

    __enabled__ = True

    _child_node_type = Property

    name: str

    def __new__(cls, *args: Any, **kwargs: Any) -> GameObject:
        """Create new GameObject instance."""
        obj = super().__new__(cls, *args, **kwargs)
        print(*obj.__children__, sep="\n")
        for child in obj.__children__:
            print(child)
            child.set_value()
        return obj

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

    def update(self, delta_time: int) -> None:
        """Update game object."""
        # play animations
        pass

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        """Draw a game object on a screen.

        :param pg.Surface screen: Target screen.
        """
        raise NotImplementedError()

    def __bool__(self) -> bool:
        """Get a bool value of the GameObject.

        The GameObject is True if it is enabled, False otherwise.
        """
        return self.__enabled__

    def accept_notification(self) -> None:
        """Accept a notification from a child property."""
        self.build()

    @abc.abstractmethod
    def build(self) -> None:
        """Build game object."""
        raise NotImplementedError()

    def __get__(
        self,
        instance: Scene,
        owner: type[Scene] | None = None,
    ) -> GameObject:
        """Get game object property.

        Returns the descriptor object itself.

        :param Scene instance: Scene instance that has the property.
        :param type[Scene] owner: Instance class. Always should be Scene type.

        :return: A game object descriptor instance.
        :rtype: GameObject
        """
        return self

    def __set_name__(self, owner: type, name: str) -> None:
        """Set up object name."""
        self.name = name
