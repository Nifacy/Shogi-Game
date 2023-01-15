from functools import partial
from itertools import product
from typing import Union

from game_model.figures import Lion
from game_model.game.manager.rules import Rule, GameStateChanges
from game_model.game.model import GameStatus, GameState, Player, Position, Board


def _find_king(board: Board, owner: Player) -> Union[Position, None]:
    for x, y in product(*map(range, board.size)):
        cell = board.get_cell(Position(x, y))

        if cell.is_empty():
            continue

        figure = cell.get_figure()

        if figure.owner == owner and isinstance(figure, Lion):
            return Position(x, y)


def _check_king_absence(state: GameState, player: Player) -> bool:
    opponent = state.second_player if player == state.first_player else state.first_player
    return _find_king(state.board, opponent) is None


def _check_king_on_last_line(changes: GameStateChanges, player: Player) -> bool:
    last_king_pos = _find_king(changes.old_state.board, player)
    new_king_pos = _find_king(changes.new_state.board, player)
    line_index = 0 if player == changes.new_state.second_player else changes.new_state.board.size[1] - 1

    return last_king_pos.y == line_index and last_king_pos == new_king_pos


class WinRule(Rule):
    def execute(self, changes: GameStateChanges):
        first_player, second_player = changes.new_state.first_player, changes.new_state.second_player

        conditions = [
            partial(_check_king_absence, changes.new_state),
            partial(_check_king_on_last_line, changes)
        ]

        if any([condition(first_player) for condition in conditions]):
            changes.new_state.status = GameStatus.FIRST_PLAYER_WIN

        if any([condition(second_player) for condition in conditions]):
            changes.new_state.status = GameStatus.SECOND_PLAYER_WIN
