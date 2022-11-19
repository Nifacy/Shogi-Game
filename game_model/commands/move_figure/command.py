from game_model.commands.base.command import BaseCommand
from game_model.commands.move_figure.exceptions import NonexistentPosition, FigureDoesntExists, UnableToMoveFigure, \
    MovingOnOccupiedCell
from game_model.game.model import GameState, Position, Player
from game_model.game.model.board import UnavailablePosition, Board


class MoveFigure(BaseCommand):
    _start_position: Position
    _end_position: Position

    def __init__(self, player: Player, start: Position, end: Position):
        super().__init__(player)
        self._start_position = start
        self._end_position = end

    def _get_cell(self, board: Board, position: Position):
        try:
            return board.get_cell(position)
        except UnavailablePosition:
            raise NonexistentPosition(player=self._player, start=self._start_position, end=self._end_position, position=position)

    def _check_figure_existence(self, board: Board, position: Position):
        if board.get_cell(position).is_empty():
            raise FigureDoesntExists(player=self._player, start=self._start_position, end=self._end_position, position=position)

    def action(self, state: GameState):
        end_cell = self._get_cell(board=state.board, position=self._end_position)
        start_cell = self._get_cell(board=state.board, position=self._start_position)
        self._check_figure_existence(state.board, self._start_position)

        figure = start_cell.get_figure()
        move_direction = Position(
            x=self._end_position.x - self._start_position.x,
            y=self._end_position.y - self._start_position.y
        )

        if not figure.can_move(move_direction):
            raise UnableToMoveFigure(player=self._player, start=self._start_position, end=self._end_position, position=move_direction, figure=figure)

        if not end_cell.is_empty() and end_cell.get_figure().owner == figure.owner:
            raise MovingOnOccupiedCell(player=self._player, start=self._start_position, end=self._end_position, position=self._end_position)

        start_cell.remove_figure()
        end_cell.put_figure(figure=figure)
