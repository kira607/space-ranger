from __future__ import annotations

import inspect

from ._property import Property


class PropertiesObserver:
    """A base class for classes that use properties.

    Properties observer recieves a notification via `PropertiesObserver._accept_notification`
    each time a property value is changed if property is set to propagate updates.
    """

    def __new__(cls) -> PropertiesObserver:
        """Construct observer.

        Scans class for properties and calls `on_collect()` for each property found.
        """
        obj = super().__new__(cls)
        for _, prop in inspect.getmembers(obj.__class__, lambda p: isinstance(p, Property)):
            prop.on_collect(obj)
        return obj

    def _accept_notification(self) -> None:
        """Accept a notification from a publisher."""
        raise NotImplementedError()
