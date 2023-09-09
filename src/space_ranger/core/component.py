from __future__ import annotations

import typing as t
from inspect import getmembers

from .property import PropertyDescriptor, PropertyHolder


class Component:
    """Game object component."""

    __properties__: list[PropertyHolder]

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> Component:
        """Construct a component object."""
        obj = super().__new__(cls)
        obj.__properties__ = []
        for name, descriptor in getmembers(obj.__class__, lambda p: isinstance(p, PropertyDescriptor)):
            if not name.startswith("_"):
                holder = descriptor.__holder_type__(descriptor.default)
                setattr(obj, descriptor.name, holder)
                holder.bind_component(obj)
                obj.__properties__.append(holder)
                descriptor.reset_default()
        return obj

    def on_property_change(self):
        pass
