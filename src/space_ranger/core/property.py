from __future__ import annotations
from pathlib import Path

import typing as t

import pygame as pg

from space_ranger.asset.font_asset import FontAsset, FontFactory

from .common import Descriptor

if t.TYPE_CHECKING:
    from .component import Component
    from .game_object import GameObject


__all__ = [
    "Bool",
    "Int",
    "Float",
    "Angle",
    "String",
    "Color",
]


_TPropertyValue = t.TypeVar("_TPropertyValue")
_TPropertyInput = t.TypeVar("_TPropertyInput")


class Property(
    Descriptor[
        type["Component"] | type["GameObject"],
        t.Union["Component", "GameObject"],
        _TPropertyValue,
        _TPropertyInput,
    ],
):
    """A :class:`space_ranger.core.Component` or :class:`space_ranger.core.GameObject` property.

    This is a base class to be used to create
    properties for components and game objects.

    :param default: Default value of the property.
    :type default: _TPropertyValue
    """

    value_type = _TPropertyValue
    input_type = _TPropertyInput

    def __init__(self, default: _TPropertyInput) -> None:
        super().__init__()
        self.default = self.adapt(default)

    def on_collect(self, instance: Component | GameObject) -> None:
        """Set a default value of the property.

        Creates an instance attribute and sets its value to default
        when instance is created.

        :param instance: A :class:`space_ranger.core.Component` or :class:`space_ranger.core.GameObject` instance.
        :type instance: Component | GameObject
        """
        setattr(instance, self.name, self.default)


_TBoolValue = bool
_TBoolInput = bool


class Bool(Property[_TBoolValue, _TBoolInput]):
    """An integer property.

    :param default: Initial value, defaults to False.
    :type default: _TBoolInput
    """

    value_type = _TBoolValue
    input_type = _TBoolInput

    def __init__(self, default: _TBoolInput = False) -> None:
        super().__init__(default)

    def adapt(self, value: _TBoolInput) -> _TBoolValue:  # noqa: D102
        return bool(value)


_TIntValue = int
_TIntInput = int | float


class Int(Property[_TIntValue, _TIntInput]):
    """An integer property.

    :param default: Initial value, defaults to 0.
    :type default: _TIntInput
    """

    value_type = _TIntValue
    input_type = _TIntInput
    lowest = None
    highest = None

    def __init__(
        self,
        default: _TIntInput = 0,
        lowest: _TIntInput | None = None,
        highest: _TIntInput | None = None,
    ) -> None:
        super().__init__(default)
        self.lowest = lowest
        self.highest = highest

    def adapt(self, value: _TIntInput) -> _TIntValue:  # noqa: D102
        return int(self.opt_clamp(int(value)))
    
    def opt_clamp(self, value: _TIntValue) -> _TIntValue:
        if self.lowest is None:
            if self.highest is None:
                return value
            return min(value, self.highest)
        if self.highest is None:
            return max(value, self.lowest)
        return pg.math.clamp(value, self.lowest, self.highest)


_TFloatValue = float
_TFloatInput = int | float


class Float(Property[_TFloatValue, _TFloatInput]):
    """A float property.

    :param default: Initial value, defaults to 0.0.
    :type default: _TFloatInput
    """

    value_type = _TFloatValue
    input_type = _TFloatInput
    lowest = None
    highest = None

    def __init__(
        self,
        default: _TFloatInput = 0.0,
        lowest: _TFloatInput | None = None,
        highest: _TFloatInput | None = None,
    ) -> None:
        super().__init__(default)
        self.lowest = lowest
        self.highest = highest

    def adapt(self, value: _TFloatInput) -> _TFloatValue:  # noqa: D102
        return float(self.opt_clamp(float(value)))
    
    def opt_clamp(self, value: _TFloatValue) -> _TFloatValue:
        if self.lowest is None:
            if self.highest is None:
                return value
            return min(value, self.highest)
        if self.highest is None:
            return max(value, self.lowest)
        return pg.math.clamp(value, self.lowest, self.highest)
    

class Angle(Float):
    """An angle property.

    Holds angle value in degrees [0.0, 360.0]

    :param default: Initial value, defaults to 0.0.
    :type default: _TFloatInput
    """

    value_type = _TFloatValue
    input_type = _TFloatInput

    def adapt(self, value: _TFloatInput) -> _TFloatValue:
        value = float(value)
        if value < 0:
            return 0.0
        return value % 360.0


_TStringValue = str
_TStringInput = str | t.Any


class String(Property[_TStringValue, _TStringInput]):
    """An string property.

    :param default: Initial value, defaults to "".
    :type default: _TStringInput
    """

    value_type = _TStringValue
    input_type = _TStringInput

    def __init__(self, default: _TStringInput = "") -> None:
        super().__init__(default)

    def adapt(self, value: _TStringInput) -> _TStringValue:  # noqa: D102
        return str(value)


_TColorValue = pg.Color
_TColorInput = pg.Color | tuple[int, int, int, int] | tuple[int, int, int] | int


class Color(Property[_TColorValue, _TColorInput]):
    """A color property.

    :param default: Initial value, defaults to black (`pygame.Color(0, 0, 0, 255)`).
    :type default: _TColorInput
    """

    value_type = _TColorValue
    input_type = _TColorInput

    def __init__(self, default: _TColorInput = 0) -> None:
        super().__init__(default)

    def adapt(self, value: _TColorInput) -> _TColorValue:  # noqa: D102
        if isinstance(value, _TColorValue):
            return value
        if isinstance(value, int):
            return pg.Color(value, value, value)
        return pg.Color(*value)


_TFontValue = FontFactory
_TFontInput = FontFactory | FontAsset | Path | str | None


class Font(Property[_TFontValue, _TFontInput]):
    """A font property.

    :param default: Initial value, defaults to None.
    :type default: _TFontInput
    """

    value_type = _TFontValue
    input_type = _TFontInput

    def __init__(self, default: _TFontInput = None) -> None:
        super().__init__(default)

    def adapt(self, value: _TFontInput) -> _TFontValue:
        if value is None:
            return FontFactory(None)
        if isinstance(value, Path | str):
            return FontAsset(value).load()
        return value
