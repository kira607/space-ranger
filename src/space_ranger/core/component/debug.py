from dataclasses import dataclass

from ._component import Component


@dataclass(slots=True)
class Debug(Component):
    pass
