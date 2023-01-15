from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import Player


class OutOfTurn(ExecuteCommandException):
    __msg_template = "Игрок {player} сейчас не может ходить"

    def __init__(self, player: Player):
        super().__init__(player, self.__msg_template.format(player=player))


class UnknownPlayer(ExecuteCommandException):
    __msg_template = "Игрок {player} не участвует в данной игре"

    def __init__(self, player: Player):
        super().__init__(player, self.__msg_template.format(player=player))


class GameEnded(ExecuteCommandException):
    __msg_template = "Игра окончена"

    def __init__(self, player: Player):
        super().__init__(player, self.__msg_template)
