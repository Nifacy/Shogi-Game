from abc import ABC, abstractmethod

from game_model.game.model import Player, GameState


class Command(ABC):
    _player: Player

    def __init__(self, player: Player):
        self._player = player

    @abstractmethod
    def execute(self, state: GameState):
        pass
