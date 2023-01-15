from copy import deepcopy
from itertools import product

from game_model.game.manager.rules import Rule, GameStateChanges
from game_model.game.model import Position, Figure, GameState, Player, Prison


def _get_prison(state: GameState, player: Player) -> Prison:
    if state.first_player == player:
        return state.first_player_prison

    return state.second_player_prison


class CaptureFigureRule(Rule):
    def execute(self, changes: GameStateChanges):
        old_board = changes.old_state.board
        new_board = changes.new_state.board

        for x, y in product(*map(range, old_board.size)):
            pos = Position(x=x, y=y)
            old_cell = old_board.get_cell(pos)
            new_cell = new_board.get_cell(pos)

            if old_cell.is_empty() or new_cell.is_empty():
                continue

            old_figure = old_cell.get_figure()
            placed_figure = new_cell.get_figure()

            if old_figure == placed_figure:
                continue

            captured_figure = deepcopy(old_figure)
            prison = _get_prison(changes.new_state, placed_figure.owner)
            prison.add_figure(old_figure)
