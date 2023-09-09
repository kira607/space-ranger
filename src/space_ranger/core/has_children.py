from __future__ import annotations

import typing as t

_TNodeChild = t.TypeVar("_TNodeChild")


class HasChildren(t.Generic[_TNodeChild]):
    """Has children."""

    __children__: list[_TNodeChild]

    _child_node_type: type[t.Any]

    def __new__(cls, *args, **kwargs) -> HasChildren[_TNodeChild]:
        """Create new instance of Scene."""
        obj = super().__new__(cls)
        obj.__children__ = []
        for k in dir(obj.__class__):
            v = getattr(obj.__class__, k)
            if isinstance(v, cls._child_node_type) and not k.startswith("_"):
                obj.__children__.append(v)
        return obj
