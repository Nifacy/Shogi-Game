from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import Position, Player, Figure


class CellOccupied(ExecuteCommandException):
    __msg_template = "Невозможно поставить фигуру на позицию {position}. Клетка уже занята"
    _position: Position

    def __init__(self, player: Player, position: Position):
        super().__init__(player, self.__msg_template.format(position=position))
        self._position = position

    @property
    def position(self) -> Position:
        return self._position


class SettingOnNonexistentPosition(ExecuteCommandException):
    __msg_template = "Невозможно поставить фигуру на несуществующую позицию {position}"
    _position: Position

    def __init__(self, player: Player, position: Position):
        super().__init__(player, self.__msg_template.format(position=position))
        self._position = position

    @property
    def position(self) -> Position:
        return self._position


class FigureDoesntExist(ExecuteCommandException):
    __msg_template = "Фигуры {figure} нет в плену игрока {player}"
    _figure: Figure

    def __init__(self, player: Player, figure: Figure):
        super().__init__(player, self.__msg_template.format(figure=figure, player=player))
        self._figure = figure

    @property
    def figure(self) -> Figure:
        return self._figure
