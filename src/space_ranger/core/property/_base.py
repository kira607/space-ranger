from __future__ import annotations

import abc
import typing as t

import numpy as np

if t.TYPE_CHECKING:
    from space_ranger.core.properties_observer import PropertiesObserver

_TPropertyValue = t.TypeVar("_TPropertyValue")
_TPropertyInput = t.TypeVar("_TPropertyInput")


class Property(t.Generic[_TPropertyValue, _TPropertyInput], abc.ABC):
    """A property.

    This is a base class to be used to create properties.

    Properties are connected to classes of type :class:`Observer`
    and should be used only within them.

    :param default: Default value of the property.
    :type default: _TPropertyInput
    """

    __animatable__ = False

    def __init__(self, default: _TPropertyInput) -> None:
        self.public_name: str
        self.name: str
        self.default = self.adapt(default)

    def __get__(
        self,
        instance: PropertiesObserver | None,
        owner: type[PropertiesObserver] | None = None,
    ) -> _TPropertyValue | Property | None:
        """Get value.

        :param instance: Object instance that has the property.
        :type instance: PropertiesObserver | None
        :param owner: Instance class/type.
        :type owner: type[PropertiesObserver] | None

        :return: Property value if accessed from class instance,
          :class:`Property` descriptor instance otherwise.
          If property attribute is not instantiated at instance returns None.
        :rtype: _TPropertyValue | Property | None
        """
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance: PropertiesObserver | None, value: _TPropertyValue) -> None:
        """Set value.

        This will notify parent :class:`Observer` instance
        using `instance.accept_notification()`.

        :param instance: Instance that has the property.
        :type instance: PropertiesObserver
        :param value: A new value of the attribute.
        :type value: _TPropertyValue
        """
        new_value = self.adapt(value)
        setattr(instance, self.name, new_value)
        instance._accept_notification()

    def __set_name__(self, owner: type[PropertiesObserver], name: str) -> None:
        """Set property name.

        Uses name to create a protected object attribute
        which is later accessed using this property descriptor.

        Neither protected nor private properties names
        are not allowed. This means that property name should
        not start with "_".

        :param type owner: PropertiesObserver class.
        :type owner: type[PropertiesObserver]
        :param name: Property name.
        :type name: str

        :raises RuntimeError: If property name starts with "_".
        """
        if name.startswith("_"):
            raise RuntimeError(f"Protected {self.__class__.__name__} names are forbidden: {name}")
        self.public_name = name
        self.name = f"_{name}"

    def __str__(self) -> str:
        """Get string representation of the property."""
        return f"{self.__class__.__name__}('{self.public_name}')"

    def __repr__(self) -> str:
        """Get object string representation of the property."""
        return f"<{str(self)}>"

    def on_collect(self, instance: PropertiesObserver) -> None:
        """Set a default value of the property.

        Creates an instance attribute and sets its value to default
        when instance is created.

        :param instance: A :class:`PropertiesObserver` instance.
        :type instance: PropertiesObserver
        """
        setattr(instance, self.name, self.default)

    @classmethod
    def adapt(cls, value: _TPropertyInput) -> _TPropertyValue:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: _TPropertyInput

        :return: Value of correct type.
        :rtype: _TPropertyValue
        """
        return value

    @classmethod
    @abc.abstractmethod
    def to_array(cls, value: _TPropertyValue) -> np.ndarray:
        """Convert value to a numpy array."""
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_array(cls, array: np.ndarray) -> _TPropertyValue:
        """Convert a numpy array to value."""
        raise NotImplementedError()
