from typing import Dict
from services.searcher_service.domain import adapters, models


# TODO: Move on Redis realization
class DefaultStorage(adapters.WaitingPlayersStorage):
    _storage: Dict[str, models.WaitingPlayer]

    def __init__(self):
        self._storage = dict()

    async def add_player(self, player: models.WaitingPlayer):
        if player.name in self._storage:
            raise adapters.AlreadyExists(player)

        self._storage[player.name] = player

    async def remove_player(self, player: models.WaitingPlayer):
        if player.name not in self._storage:
            raise adapters.NotExists(player)

        del self._storage[player.name]

    async def find_opponent(self, player: models.WaitingPlayer) -> models.WaitingPlayer | None:
        for opponent in self._storage.values():
            if opponent.name != player.name and player.check_opponent(opponent):
                return opponent
