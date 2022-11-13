from typing import Iterable

from game_model.figures.base import BaseFigure
from game_model.figures.directions import MoveDirection
from game_model.game.model import Position


class Elephant(BaseFigure):
    def get_enable_positions(self) -> Iterable[Position]:
        return set(map(
            lambda el: el.value,
            [
                MoveDirection.DOWN_LEFT,
                MoveDirection.DOWN_RIGHT,
                MoveDirection.UP_LEFT,
                MoveDirection.UP_RIGHT
            ]
        ))
