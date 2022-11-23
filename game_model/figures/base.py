from abc import ABC, abstractmethod
from typing import Iterable

from game_model.game.model import Figure, Position, Player


class BaseFigure(Figure, ABC):
    def __init__(self, owner: Player):
        super().__init__(owner=owner)

    @abstractmethod
    def get_enable_positions(self) -> Iterable[Position]:
        pass

    def can_move(self, direction: Position) -> bool:
        enable_positions = self.get_enable_positions()
        return direction in enable_positions
