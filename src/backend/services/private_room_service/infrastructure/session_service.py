from typing import Iterable

from contracts import session_service
from rpc_service import RpcClientBuilder
from ..domain import adapters, models


class SessionServiceClient(adapters.SessionServiceAdapter):
    def __init__(self):
        self._client = RpcClientBuilder.from_contract(session_service.Contract)

    async def create_session(self, players: Iterable[models.Player]) -> adapters.Session:
        first_player, second_player = map(lambda player: player.name, players)
        response = await self._client.create_session(first_player=first_player, second_player=second_player)
        return adapters.Session(id=response.session_id)

    async def connect(self, credentials: str):
        await self._client.connect(credentials)

    async def close(self):
        await self._client.close()
