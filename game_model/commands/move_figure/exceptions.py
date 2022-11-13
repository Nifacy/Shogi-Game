from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import Player, Position, Figure


class MoveFigureException(ExecuteCommandException):
    _start_position: Position
    _end_position: Position

    def __init__(self, player: Player, start: Position, end: Position, message_template: str):
        formatted_message = message_template.format(
            player=player,
            start_position=start,
            end_position=end,
        )

        super().__init__(player=player, message=formatted_message)
        self._start_position = start
        self._end_position = end

    @property
    def start_position(self) -> Position:
        return self._start_position

    @property
    def end_position(self) -> Position:
        return self._end_position


class NonexistentPosition(MoveFigureException):
    __msg_template = "Позиции {position} не существует"

    def __init__(self, player: Player, start: Position, end: Position):
        super().__init__(player, start, end, self.__msg_template)


class FigureDoesntExists(ExecuteCommandException):
    __msg_template = "Нет фигуры на позиции {position}"
    _position: Position

    def __init__(self, player: Player, start: Position, end: Position):
        super().__init__(player, self.__msg_template.format(position=position))
        self._position = position

    @property
    def position(self) -> Position:
        return self._position


class UnableToMoveFigure(ExecuteCommandException):
    __msg_template = "Фигура {figure} не может передвигаться на позицию {position}"
    _figure: Figure
    _position: Position

    def __init__(self, player: Player, figure: Figure, position: Position):
        super().__init__(player, self.__msg_template.format(figure=figure, position=position))
        self._figure = figure
        self._position = position

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def position(self) -> Position:
        return self._position


class MovingOnOccupiedCell(ExecuteCommandException):
    __msg_template = "Клетка на позиции {position} уже занята дружественной фигурой"
    _position: Position

    def __init__(self, player: Player, position: Position):
        super().__init__(player, self.__msg_template.format(position=position))
        self._position = position

    @property
    def position(self) -> Position:
        return self._position
