from typing import Sequence

from pygame import Vector2

PositionValue = int | float
PositionSequence = Sequence[PositionValue]
TPosition = Vector2 | PositionSequence
