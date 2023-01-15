from contracts import searcher_service
from contracts.searcher_service import CallerInfo, SearchParameters
from services.searcher_service import domain
from services.searcher_service.domain import models, adapters


class Implementation(searcher_service.Contract):
    def __init__(self, database: adapters.WaitingPlayersStorage, client: adapters.SessionServiceAdapter):
        self._database = database
        self._client = client

    @staticmethod
    def _serialize_player(caller: CallerInfo, parameters: SearchParameters):
        params = models.SearchParameters(min_rating=parameters.min_rating, max_rating=parameters.max_rating)
        player = models.WaitingPlayer(name=caller.name, rating=caller.rating, parameters=params)

        return player

    async def start_search(self, caller: CallerInfo, parameters: SearchParameters):
        try:
            player = self._serialize_player(caller, parameters)
            await domain.StartSearch(self._database, self._client)(player)

        except adapters.AlreadyExists:
            raise searcher_service.SearchAlreadyStarted(caller=caller)

    async def cancel_search(self, caller: CallerInfo):
        try:
            player = self._serialize_player(caller, searcher_service.SearchParameters(min_rating=0, max_rating=0))
            await domain.CancelSearch(self._database)(player)

        except adapters.NotExists:
            raise searcher_service.SearchNotStarted(caller=caller)
