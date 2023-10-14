import typing as t

import numpy as np
import pygame as pg

from .game_object import GameObject
from .logging import LoggerMixin
from .property import Property

_TAnimatedValue = t.TypeVar("_TAnimatedValue")
AnimationParams: t.TypeAlias = tuple[
    GameObject,
    str,
    Property,
    _TAnimatedValue,
    _TAnimatedValue,
    t.Callable[[float], float] | None,
    int | None,
    int | None,
]


class SingleAnimation(t.Generic[_TAnimatedValue], LoggerMixin):
    """A base animation."""

    def __init__(
        self,
        game_object: GameObject,
        property_name: str,
        property_type: Property,
        start_value: _TAnimatedValue,
        final_value: _TAnimatedValue,
        interpolate: t.Callable[[float], float] | None = None,
        duration: int | None = None,
        offset: int | None = None,
    ) -> None:
        self._game_object = game_object
        self._property_name = property_name
        self._property_type = property_type
        self._start_value = start_value
        self._final_value = final_value
        self._interpolate = interpolate or (lambda x: x)
        self._duration = int(max(duration or 0, 0))
        self._offset = int(pg.math.clamp(offset or 0, 0, self._duration))

        # compute vectors
        self._a: np.ndarray
        self._b: np.ndarray
        self._c: np.ndarray

        self._progress = self._offset

        self._compute_vectors()

    def play(self, delta_time: int) -> None:
        """Play the animation.

        This will update game object property with new value.

        :param int delta_time: Delta time (in milliseconds).
        """
        # force finished animation to use final value
        if self.is_finished:
            self._update(self._final_value)
            return

        self._progress = self._progress + delta_time

        result = self._property_type.from_array(self._a + self._c * self._interpolate(self.progress))
        self._update(result)

    @property
    def progress(self) -> float:
        """Normilized animation progress value ([0, 1]).

        :return: Normalized animation progress value.
        :rtype: float
        """
        if self._duration == 0:
            return 1
        return pg.math.clamp(self._progress / max(self._duration, 1), 0, 1)

    @property
    def is_finished(self) -> bool:
        """Get is the animation finished.

        Animation is finished, when its progress is >= 1.

        :return: Whether the animation is finished.
        :rtype: bool
        """
        return self.progress >= 1

    def reset(self) -> None:
        """Reset animation progress to 0.

        This will start animation over again.
        """
        self._progress = 0

    def flip(self) -> None:
        """Flip animation direction.

        Allows to play animation backwards.
        The duration of backward animation is the same as forward animation.
        """
        self._start_value, self._final_value = self._final_value, self._start_value
        self._progress = self._duration - pg.math.clamp(self._progress, 0, self._duration)
        self._compute_vectors()

    def _compute_vectors(self) -> None:
        """Compute animation vectors."""
        self._a = self._property_type.to_array(self._start_value)
        self._b = self._property_type.to_array(self._final_value)
        self._c = self._b - self._a

    def _update(self, value: _TAnimatedValue) -> None:
        """Update game object property with new value.

        :param value: New value of the game object property.
        :type value: _TAnimatedValue

        :return: None
        :rtype: None
        """
        setattr(self._game_object, self._property_name, value)


class Animation:
    """Animation.

    :param GameObjectProperty[T] source: Game object property to animate.
    :param T target: A final value after animation is finished.
    :param int duration: A duration of the animation (milliseconds).
      Set to 0 to make animation run instantly from start to finish.
      defaults to 0.
    :param Interpolation interpolate: An interpolation function to apply.
      Interpolation function is applied to a normalized ([0, 1])
      animation progress and defines how game object property will interpolate
      during animation. Interpolation function is forced to clam between [0, 1].
      defaults to LinearIterpolation.
    """

    def __init__(
        self,
        *animations: AnimationParams,
        interpolate: t.Callable[[float], float] | None = None,
        duration: int | None = None,
        offset: int | None = None,
    ) -> None:
        self.animations = [
            SingleAnimation(*args, interpolate=interpolate, duration=duration, offset=offset) for args in animations
        ]

    def play(self, delta_time: int) -> _TAnimatedValue:
        """Play the animation.

        :param int delta_time: Delta time (in milliseconds).
        """
        for animation in self.animations:
            animation.play(delta_time)


class HoverAnimation(Animation):
    """Hover animation."""

    def __init__(
        self,
        *animations: AnimationParams,
        interpolate: t.Callable[[float], float] | None = None,
        duration: int | None = None,
        offset: int | None = None,
    ) -> None:
        super().__init__(*animations, interpolate=interpolate, duration=duration, offset=offset)
        for animation in self.animations:
            animation.flip()
        self._hovering = False

    def play(self, delta_time: int, hovering: bool = False) -> _TAnimatedValue:
        """Play animation."""
        hovering_changed = not (self._hovering is hovering)
        self._hovering = hovering

        if hovering_changed:
            for animation in self.animations:
                animation.flip()

        super().play(delta_time)
        for animation in self.animations:
            animation.play(delta_time)
