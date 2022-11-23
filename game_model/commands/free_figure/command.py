from .exceptions import *
from game_model.commands.base.command import BaseCommand
from game_model.game.model import GameState, Position, Player, Figure, Prison
from game_model.game.model.board import UnavailablePosition


class FreeFigure(BaseCommand):
    _figure: Figure
    _position: Position

    def __init__(self, player: Player, figure: Figure, put_position: Position):
        super().__init__(player=player)
        self._figure = figure
        self._position = put_position

    def _get_prison(self, state: GameState) -> Prison:
        if self._player == state.first_player:
            return state.first_player_prison

        return state.second_player_prison

    def action(self, state: GameState):
        prison = self._get_prison(state)

        if self._figure not in prison.figures:
            raise FigureDoesntExist(player=self._player, figure=self._figure)

        try:
            cell = state.board.get_cell(self._position)
        except UnavailablePosition:
            raise SettingOnNonexistentPosition(player=self._player, position=self._position)

        if not cell.is_empty():
            raise CellOccupied(player=self._player, position=self._position)

        prison.remove_figure(self._figure)
        cell.put_figure(self._figure)
