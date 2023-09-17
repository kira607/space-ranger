from __future__ import annotations

import abc
import inspect
import typing as t

from .property import Property


class PropertiesObserver(abc.ABC):
    """A base class for classes that use properties.

    Properties observer recieves a notification via `PropertiesObserver._accept_notification`
    each time a property value is changed.
    """

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> PropertiesObserver:
        """Construct collector."""
        obj = super().__new__(cls)
        for _, prop in inspect.getmembers(obj.__class__, lambda p: isinstance(p, Property)):
            prop.on_collect(obj)
        return obj

    @abc.abstractmethod
    def _accept_notification(self) -> None:
        """Accept a notification from a publisher."""
        raise NotImplementedError()
