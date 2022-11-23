from game_model.game.manager.rules import Rule, GameStateChanges
from game_model.game.model import GameStatus


class ChangePlayerTurnRule(Rule):
    _new_status_map = {
        GameStatus.FIRST_PLAYER_TURN: GameStatus.SECOND_PLAYER_TURN,
        GameStatus.SECOND_PLAYER_TURN: GameStatus.FIRST_PLAYER_TURN
    }

    def execute(self, changes: GameStateChanges):
        old_status = changes.old_state.status

        if old_status in self._new_status_map and changes.new_state.status in self._new_status_map:
            changes.new_state.status = self._new_status_map[old_status]
