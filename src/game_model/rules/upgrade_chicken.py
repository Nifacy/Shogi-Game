from typing import Iterable

from game_model.figures import Chicken, Hen
from game_model.game.manager.rules import Rule, GameStateChanges
from game_model.game.model import Board, Figure, Position, Cell, Player


def _get_chickens(owner: Player, cells: Iterable[Cell]) -> Iterable[Cell]:
    chickens = []

    for cell in cells:
        if cell.is_empty():
            continue

        figure = cell.get_figure()

        if figure.owner == owner and isinstance(figure, Chicken):
            chickens.append(cell)

    return chickens


def _get_line(board: Board, line_index: int) -> Iterable[Cell]:
    return [board.get_cell(Position(x, line_index)) for x in range(board.size[0])]


def _upgrade_chicken(cell: Cell):
    chicken = cell.get_figure()
    hen = Hen(owner=chicken.owner)

    cell.remove_figure()
    cell.put_figure(hen)


class UpgradeChickenRule(Rule):
    def execute(self, changes: GameStateChanges):
        first_player, second_player = changes.new_state.first_player, changes.new_state.second_player
        board = changes.new_state.board
        last_index = board.size[1] - 1

        for cell in _get_chickens(second_player, _get_line(board, 0)):
            print("Upgrade")
            _upgrade_chicken(cell)

        for cell in _get_chickens(first_player, _get_line(board, last_index)):
            print("Upgrade")
            _upgrade_chicken(cell)
