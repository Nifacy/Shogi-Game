from typing import Iterable

from game_model.figures.base import BaseFigure
from game_model.figures.directions import MoveDirection
from game_model.game.model import Position


class Hen(BaseFigure):
    def get_enable_positions(self) -> Iterable[Position]:
        return set(map(
            lambda el: el.value,
            [
                MoveDirection.UP_LEFT,
                MoveDirection.UP,
                MoveDirection.UP_RIGHT,
                MoveDirection.LEFT,
                MoveDirection.RIGHT,
                MoveDirection.DOWN
            ]
        ))
