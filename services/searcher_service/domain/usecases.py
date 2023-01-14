from . import adapters, models, events


async def _notify_about_find_opponent(caller: models.WaitingPlayer, created_session: adapters.Session):
    message = events.OnFindOpponentMessage(caller=caller, created_session=created_session)
    await events.searcher_events.on_find_opponent(message)


class StartSearch:
    _storage: adapters.WaitingPlayersStorage
    _adapter: adapters.SessionServiceAdapter

    def __init__(self, storage: adapters.WaitingPlayersStorage, adapter: adapters.SessionServiceAdapter):
        self._storage = storage
        self._adapter = adapter

    async def __call__(self, caller: adapters.WaitingPlayersStorage):
        await self._storage.add_player(caller)
        opponent = await self._storage.find_opponent(caller)

        if opponent is not None:
            await self._storage.remove_player(caller)
            await self._storage.remove_player(opponent)
            session = await self._adapter.create_session((caller, opponent))
            await _notify_about_find_opponent(caller, session)
            await _notify_about_find_opponent(opponent, session)


class CancelSearch:
    _storage: adapters.WaitingPlayersStorage

    def __init__(self, storage: adapters.WaitingPlayersStorage):
        self._storage = storage

    async def __call__(self, caller: models.WaitingPlayer):
        await self._storage.remove_player(caller)
