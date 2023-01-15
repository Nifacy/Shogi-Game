from game_model.game.manager.command import Command
from game_model.game.model import GameStatus
from services.session_service.domain.adapters import SessionStorage
from services.session_service.domain.events import *
from services.session_service.domain.models import SessionModel


class CreateSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, first_player_name: str, second_player_name: str) -> SessionModel:
        session = await self._storage.create(first_player_name, second_player_name)
        print(session)
        session.disconnect(first_player_name)
        session.disconnect(second_player_name)
        await self._storage.update(session)

        return session


class ConnectToSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, player_name: str, session_id: int):
        session = await self._storage.get(session_id)
        session.connect(player_name=player_name)
        await self._storage.update(session)

        await session_events.on_player_connected(OnPlayerConnectedMessage(
            session_id=session_id,
            player_name=player_name
        ))


class DisconnectFromSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, player_name: str, session_id: int):
        session = await self._storage.get(session_id)
        await session.disconnect(player_name=player_name)
        await self._storage.update(session)

        await session_events.on_player_disconnected(OnPlayerDisconnectedMessage(
            session_id=session_id,
            player_name=player_name
        ))


class GetPlayer:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, player_name: str, session_id: int):
        session = await self._storage.get(session_id)
        return session.get_player(player_name)


class ExecuteCommand:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, session_id: int, command: Command):
        session = await self._storage.get(session_id)
        session.execute_command(command)
        await self._storage.update(session)

        await session_events.on_state_changed(OnStateChangedMessage(
            session_id=session_id,
            state=session.state
        ))

        if session.state.status == GameStatus.SECOND_PLAYER_WIN:
            await session_events.on_game_ended(OnGameEndedMessage(
                session_id=session.id,
                winner=session.get_players()[1]
            ))
            await self._storage.remove(session_id)

        if session.state.status == GameStatus.FIRST_PLAYER_WIN:
            await session_events.on_game_ended(OnGameEndedMessage(
                session_id=session.id,
                winner=session.get_players()[0]
            ))
            await self._storage.remove(session_id)


class GetSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, session_id: int) -> SessionModel:
        return await self._storage.get(session_id)
