from abc import ABC, abstractmethod
from .. import models


class AlreadyExists(Exception):
    player: models.WaitingPlayer
    _message: str = 'Player {player_name!r} already waiting for opponent'

    def __init__(self, player: models.WaitingPlayer):
        super().__init__(self._message.format(player_name=player.name))
        self.player = player


class NotExists(Exception):
    player: models.WaitingPlayer
    _message: str = 'Player {player_name!r} not waiting for opponent'

    def __init__(self, player: models.WaitingPlayer):
        super().__init__(self._message.format(player_name=player.name))
        self.player = player


class WaitingPlayersStorage(ABC):
    @abstractmethod
    async def add_player(self, player: models.WaitingPlayer):
        raise NotImplementedError()

    @abstractmethod
    async def remove_player(self, player: models.WaitingPlayer):
        raise NotImplementedError()

    @abstractmethod
    async def find_opponent(self, player: models.WaitingPlayer) -> models.WaitingPlayer | None:
        raise NotImplementedError()
