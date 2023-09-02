import abc

import pygame as pg

from .game_object_property import GameObjectProperty, Position


class GameObject(abc.ABC):
    """A base game object.

    A game object is an observer of its properties.

    When a GameObjectProperty is chaged it notifies
    its GameObject which triggers a GameObject.on_property_change.
    """

    __properties__ = []
    __enabled__ = True

    position = Position()

    @property
    def is_enabled(self) -> bool:
        """Get if the GameObject is enabled.

        :return: Whether the GameObject is enabled.
        :rtype: bool
        """
        return bool(self)

    def __bool__(self) -> bool:
        """Get a bool value of the GameObject.

        The GameObject is True if it is enabled, False otherwise.
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

    def on_property_create(self, prop: GameObjectProperty) -> None:
        """Process an event of a GameObjectProperty creation.

        :param GameObjectProperty prop: Created GameObjectProperty instance.
        """
        self.__properties__.append(prop)

    def on_property_change(self) -> None:
        """Process an event of a GameObjectProperty change."""
        self.build()

    @abc.abstractmethod
    def build(self) -> None:
        """Rebuild a game object."""
        raise NotImplementedError()

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        """Draw a game object on a screen.

        :param pg.Surface screen: Target screen.
        """
        raise NotImplementedError()

    def _draw(self, screen: pg.Surface) -> None:
        """Draw a game object on a screen.

        Does not draw the game object if it is disabled.

        :param pg.Surface screen: Target screen.
        """
        if not self.is_enabled:
            return
        self.draw()
