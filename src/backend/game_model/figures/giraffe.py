from typing import Iterable

from game_model.figures.base import BaseFigure
from game_model.figures.directions import MoveDirection
from game_model.game.model import Position


class Giraffe(BaseFigure):
    def get_enable_positions(self) -> Iterable[Position]:
        return set(map(
            lambda el: el.value,
            [
                MoveDirection.UP,
                MoveDirection.DOWN,
                MoveDirection.LEFT,
                MoveDirection.RIGHT
            ]
        ))
