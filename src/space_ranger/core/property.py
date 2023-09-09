from __future__ import annotations

import abc
import typing as t

from space_ranger.logging import LoggerMixin

if t.TYPE_CHECKING:
    from .component import Component

_TComponent = t.TypeVar("_TComponent", bound=Component)
_TPropertyValue = t.TypeVar("_TPropertyValue")


# holds component property value
# on change triggers parent component to update
# stays at instance level under protected name
# accessed using property descriptor
class PropertyHolder(t.Generic[_TPropertyValue], LoggerMixin):
    """A component property."""

    __component__: Component
    __default__: _TPropertyValue
    __animatable__: bool = False

    def __init__(self, value: _TPropertyValue) -> None:
        self._value = value

    def get_value(self) -> _TPropertyValue:
        """Get property value."""
        return self._value

    def set_value(self, value: _TPropertyValue) -> None:
        """Set property value."""
        self._value = value
        self.__component__.on_property_change()

    def bind_component(self, component: _TComponent) -> None:
        """Bind property holder to a component instance."""
        self.__component__ = component


class PropertyDescriptor(t.Generic[_TPropertyValue], LoggerMixin, abc.ABC):
    """A base component property.

    Property holds exactly one value.
    A set of properties describes a component state

    :param _TPropertyValue | None, optional default: Default value of the property, defaults to None.
    """

    __holder_type__: type[PropertyHolder] = PropertyHolder

    def __init__(self, default: _TPropertyValue | None = None) -> None:
        self.name: str
        self.default = default

    def __get__(
        self,
        instance: Component | None,
        owner: type[Component] | None = None,
    ) -> PropertyHolder[_TPropertyValue]:
        """Get component property.

        Returns the descriptor object itself.

        :param Component instance: Component instance that has the property.
        :param type[Component] owner: Instance class. Should be Component type or its subclass.

        :return: A component property descriptor instance.
        :rtype: GameObjectProperty[_TPropertyValue]
        """
        if instance is None:
            return self
        return self.get_holder(instance)

    def __set__(self, instance: Component, value: _TPropertyValue) -> None:
        """Set component property value.

        Uses :class:`GameObjectProperty.value` setter.

        :param GOTNode[PT, CT, VT] instance: Object instance that has the property.
        :param T value: A new value of the property.
        """
        holder = self.get_holder(instance)
        holder.set_value(value)

    def __set_name__(self, owner: type, name: str) -> None:
        """Set name."""
        self.name = f"_{name}"

    def get_holder(self, instance: Component) -> PropertyHolder:
        """Get property value holder at instance."""
        return getattr(instance, self.name)

    def reset_default(self) -> None:
        """Reset the default value to None."""
        self.default = None
