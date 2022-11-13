from game_model.game.model import Player


class ExecuteCommandException(Exception):
    _player: Player
    __msg_template: str = "Невозможно выполнить команду игрока {player}: {msg}"

    def __init__(self, player: Player, message: str):
        super().__init__(self.__msg_template.format(player=player, msg=message))
        self._player = player

    @property
    def player(self) -> Player:
        return self._player
