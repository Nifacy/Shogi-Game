from abc import ABC, abstractmethod

from game_model.game.manager.rules.game_state_changes import GameStateChanges


class Rule(ABC):
    @abstractmethod
    def execute(self, changes: GameStateChanges):
        pass
