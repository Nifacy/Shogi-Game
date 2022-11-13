from typing import Iterable

from game_model.figures.base import BaseFigure
from game_model.figures.directions import MoveDirection
from game_model.game.model import Position


class Chicken(BaseFigure):
    def get_enable_positions(self) -> Iterable[Position]:
        return {MoveDirection.UP.value}
