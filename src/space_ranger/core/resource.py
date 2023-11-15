from __future__ import annotations

import typing as t
from dataclasses import dataclass

from .utils import MISSING


@dataclass(slots=True)
class Resource:
    """A resource.

    A resource is an object shared between scenes
    an has more of like a global varable vibe.
    Like a component, resource is just
    a piece of named data, except resource
    it not attached to a certain entity
    but is a "component" of the application
    itself.

    Resource is defined by its key.
    The key of a resource is its type/class.

    Resources are stored at application level
    and can be accessed at any time by systems.

    Use cases for a resource:
    * Application window
    * Game settings
    * Player controlls
    * Clock / delta time
    * Events
    * etc.
    """

    @classmethod
    def get_key(cls) -> type[Resource]:
        """Get a resource key.

        :return type[Resource]: A resource key.
        """
        return cls


ResourceKey: t.TypeAlias = type[Resource]


class ApplicationResources:
    """Application resources storage.

    This is a simple map with (:ref:`ResourceKey` -> :class:`Resource`)
    pairs, providing an interface for accessing
    application resources.
    """

    def __init__(self) -> None:
        self._resources: dict[ResourceKey, Resource] = {}

    def get_resource(self, key: ResourceKey, default: t.Any = MISSING) -> Resource | t.Any:
        """Get a resource by key.

        :param ResourceKey key: A key of the resource.
        :param t.Any default: A default value to return
            if a resource with the given key does not exist, defaults to MISSING.

        :raises UnknownResourceKeyError: A resource with the given key doesn't exist
            and a default value wasn't specified.

        :return Resource | t.Any: A resource object with the given key.
            If a resource with the given key does not exist returns default value.
            If a default value wasn't specified raises an error.
        """
        resource = self._resources.get(key, default)
        if resource is MISSING:
            raise UnknownResourceKeyError(key)
        return resource
