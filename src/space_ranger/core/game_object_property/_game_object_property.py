from __future__ import annotations

import typing as t
from abc import ABC

if t.TYPE_CHECKING:
    from space_ranger.core import GameObject

T = t.TypeVar("T")


class GameObjectProperty(t.Generic[T], ABC):
    """A base game object property.

    :param T | None, optional default: Default value of the property, defaults to None.
    :param bool always_rebuild: Whether to rebuild the game object on property value change, defaults to True.
    """

    __animatable__: bool = False
    __default__: T | None = None  # type: ignore
    __children__ = []
    __parent__: GameObjectProperty | None = None

    def __init__(self, default: T | None = None, *, always_rebuild: bool = True) -> None:
        self._value: T = default or self.__default__
        self._always_rebuild = always_rebuild
        self._public_name: str

    @property
    def value(self) -> T:
        """Game object property value."""
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        """Set game object property value.

        :param T value: A new value of the game object property.
        """
        self.set_value(value)

    def set_value(self, value: T) -> None:
        """Set game object property value.

        :param T value: A new value of the game object property.
        """
        self._value = value

    def __get__(self, instance: GameObject, owner: type[GameObject]) -> GameObjectProperty[T]:
        """Get game object property.

        Returns the descriptor object itself.

        :param GameObjectProperty[T] instance: Object instance that has the property.
        :param type owner: Instance class.

        :return: A game object property descriptor instance.
        :rtype: GameObjectProperty[T]
        """
        return self

    def __set__(self, instance: GameObject, value: T) -> None:
        """Set game object property value.

        Uses :class:`GameObjectProperty.value` setter.

        :param GameObjectProperty[T] instance: Object instance that has the property.
        :param T value: A new value of the game object property.
        """
        self.value = value
        instance.on_property_change()

    def __set_name__(self, owner: type[GameObject], name: str) -> None:
        """Initialize game object property on set name.

        :param GameObjectProperty[T] owner: Game object class.
        :param str name: A property name.
        """
        if name.startswith("_"):
            raise ValueError("Game object property cannot start with a '_' character")

        self._public_name = name
        owner.on_porperty_create(self)
