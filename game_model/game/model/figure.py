from abc import ABC, abstractmethod

from game_model.game.model.player import Player
from game_model.game.model.id_generator import IdGenerator
from game_model.game.model.position import Position


class Figure(ABC):
    _id_generator: IdGenerator = IdGenerator()
    _id: int
    owner: Player

    def __init__(self, owner: Player):
        self._id = self._id_generator.generate_id()
        self.owner = owner

    @abstractmethod
    def can_move(self, direction: Position) -> bool:
        pass

    @staticmethod
    def equals(first: "Figure", second: "Figure") -> bool:
        return first._id == second._id

    def __eq__(self, other: "Figure") -> bool:
        return Figure.equals(self, other)
