import abc
import typing as t

import pygame as pg

from space_ranger.logging import LoggerMixin

from .property import Property


def is_animatable(obj: t.Any) -> bool:
    """Check if the object is animatable.

    :param Any obj: Object to check

    :return: Whether object is animatable.
    :rtype: bool
    """
    return all(
        (
            hasattr(obj, "__animatable__"),
            obj.__animatable__,
        ),
    )


class Interpolation(abc.ABC):
    """Interpolation interface."""

    @classmethod
    @abc.abstractmethod
    def __call__(cls, value: float) -> float:
        """Apply interpolation.

        :param float value: A value to interpolate.

        :return: Interpolated value.
        :rtype: float
        """
        raise NotImplementedError()


class LinearInterpolation:
    """A linear interpolation."""

    @classmethod
    def __call__(cls, value: float) -> float:
        """Apply linear interpolation.

        :param float value: A value to interpolate.

        :return: Interpolated value.
        :rtype: float
        """
        return value


_TAnimationTarget = t.TypeVar("_TAnimationTarget")


class Animation(t.Generic[_TAnimationTarget], LoggerMixin):
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
        source: Property,
        target: _TAnimationTarget,
        duration: int = 0,
        interpolate: Interpolation = LinearInterpolation,
    ) -> None:
        if not is_animatable(source):
            raise ValueError(f"Cannot animate {type(source).__name__}")
        self._prop = source
        self._source = source.value
        self._target = target
        self._duration = max(duration, 0)
        self._interpolate = interpolate
        self._progress = 0

    def play(self, delta_time: int) -> None:
        """Play the animation.

        :param int delta_time: Delta time (in milliseconds).
        """
        if self._duration == 0:
            self._prop = self._target
            return

        self._progress += delta_time

        if self.is_finished:
            return

        self._prop = self._source + (self._source - self._target) * pg.math.clamp(
            self._interpolate(self.progress),
            0,
            1,
        )

    @property
    def progress(self) -> float:
        """Normilized animation progress value ([0, 1]).

        :return: Normalized animation progress value.
        :rtype: bool
        """
        return pg.math.clamp(self._progress / max(self._duration, 1), 0, 1)

    @property
    def is_finished(self) -> bool:
        """Get is the animation finished.

        Animation is finished, when its progress is >= 1.

        :return: Whether the animation is finished.
        :rtype: bool
        """
        return self.progress >= 1
