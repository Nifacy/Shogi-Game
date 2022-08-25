from abc import ABC, abstractmethod

from game.model.player import Player
from game.model.id_generator import IdGenerator
from game.model.position import Position


class Figure(ABC):
    _id_generator: IdGenerator = IdGenerator()
    _id: int
    owner: Player

    def __init__(self, owner: Player):
        self._id = self._id_generator.generate_id()
        self.owner = owner

    @staticmethod
    def equals(first: "Figure", second: "Figure") -> bool:
        return first._id == second._id

    def __eq__(self, other: "Figure") -> bool:
        return self.equals(self, other)

    @abstractmethod
    def can_move(self, direction: Position) -> bool:
        pass
