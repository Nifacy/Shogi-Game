from abc import abstractmethod, ABC

from game_model.game.manager.command import Command
from game_model.game.model import GameState
from game_model.game.model.state import GameStatus


class BaseCommand(Command, ABC):
    def execute(self, state: GameState):
        if self._player not in (state.first_player, state.second_player):
            raise UnknownPlayer(self._player)

        if state.status not in (GameStatus.FIRST_PLAYER_TURN, GameStatus.SECOND_PLAYER_TURN):
            raise GameEnded(self._player)

        active_player = state.first_player if state.status == GameStatus.FIRST_PLAYER_TURN else state.second_player

        if self._player != active_player:
            raise OutOfTurn(self._player)

        self.action(state)

    @abstractmethod
    def action(self, state: GameState):
        pass
