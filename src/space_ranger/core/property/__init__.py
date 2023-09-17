"""Observer properties."""

from ._base import Property as Property
from .angle import Angle as Angle
from .bool import Bool as Bool
from .color import Color as Color
from .float import Float as Float
from .font import Font as Font
from .int import Int as Int
from .string import String as String

__all__ = [
    "Property",
    "Angle",
    "Bool",
    "Color",
    "Float",
    "Font",
    "Int",
    "String",
]
