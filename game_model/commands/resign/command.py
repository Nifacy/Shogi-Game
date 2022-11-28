from ...game.manager.command import Command
from ...game.model import GameState, Player, GameStatus


class Resign(Command):
    def execute(self, state: GameState):
        if state.first_player == self._player:
            state.status = GameStatus.SECOND_PLAYER_WIN

        if state.second_player == self._player:
            state.status = GameStatus.FIRST_PLAYER_WIN
