import typing as t

import numpy as np
import pygame as pg

from space_ranger.logging import LoggerMixin

_TAnimatedValue = t.TypeVar("_TAnimatedValue")


class Animation(t.Generic[_TAnimatedValue], LoggerMixin):
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
        x: _TAnimatedValue,
        y: _TAnimatedValue,
        to_array: t.Callable[[_TAnimatedValue], np.array],
        from_array: t.Callable[[np.array], _TAnimatedValue],
        duration: int = 0,
        offset: int = 0,
        interpolate: t.Callable[[float], float] = lambda x: x,
    ) -> None:
        self._x = x
        self._y = y
        self._to_array = to_array
        self._from_array = from_array
        self._duration = max(duration, 0)
        self._progress = max(offset, 0)
        self._f = interpolate
        self._a = to_array(self._x)
        self._b = to_array(self._y)
        self._c = self._b - self._a

    def play(self, delta_time: int, **kwargs) -> _TAnimatedValue:
        """Play the animation.

        :param int delta_time: Delta time (in milliseconds).
        """
        # zero duration animation is instant
        final_value = self._get_final_value()

        if self._duration == 0:
            return final_value

        self._update_progress(delta_time)

        # force finished animation to return final value
        if self.is_finished:
            return final_value

        # change value
        result = self._play()
        return self._from_array(result)

    def reset(self) -> None:
        """Reset animation progress to 0."""
        self._progress = 0

    @property
    def progress(self) -> float:
        """Normilized animation progress value ([0, 1]).

        :return: Normalized animation progress value.
        :rtype: float
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
    
    def _get_final_value(self):
        return self._y

    def _update_progress(self, delta_time: int) -> None:
        self._progress = self._progress + delta_time

    def _play(self):
        return np.rint(self._a + self._c * self._f(self.progress)).astype(int)


class ForwardBackAnimation(Animation[_TAnimatedValue]):
    def __init__(
        self,
        source: _TAnimatedValue,
        target: _TAnimatedValue,
        to_array: t.Callable[[_TAnimatedValue], np.array],
        from_array: t.Callable[[np.array], _TAnimatedValue],
        duration: int = 0,
        offset: int = 0,
        interpolate: t.Callable[[float], float] = lambda x: x,
    ) -> None:
        super().__init__(source, target, to_array, from_array, duration, offset, interpolate)
        self._forward = None

    def play(self, delta_time: int, forward: bool = True, **kwargs) -> _TAnimatedValue:
        if self._forward is not None:
            if self._forward is not forward:
                self._progress = pg.math.clamp(self._progress, 0, self._duration)
        self._forward = forward
        return super().play(delta_time, **kwargs)
    
    @property
    def is_finished(self) -> bool:
        if self._forward and self.progress >= 1:
            return True
        if not self._forward and self.progress <= 0:
            return True
        return False
    
    def _get_final_value(self):
        return self._y if self._forward else self._x

    def _update_progress(self, delta_time: int) -> None:
        self._progress += delta_time if self._forward else -delta_time
