from abc import ABC, abstractmethod
from typing import Iterable

from game_model.game.model import Figure, Position, Player


def _rotate_position(position: Position) -> Position:
    return Position(x=-position.x, y=-position.y)


class BaseFigure(Figure, ABC):
    _opposite_moving: bool

    def __init__(self, owner: Player, opposite_moving: bool = False):
        super().__init__(owner=owner)
        self._opposite_moving = opposite_moving

    @abstractmethod
    def get_enable_positions(self) -> Iterable[Position]:
        pass

    def can_move(self, direction: Position) -> bool:
        enable_positions = self.get_enable_positions()

        if self._opposite_moving:
            enable_positions = map(_rotate_position, enable_positions)

        return direction in enable_positions
