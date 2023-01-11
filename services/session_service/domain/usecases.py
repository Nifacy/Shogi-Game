from enum import Enum

from ddd_domain_events import DomainEvents

from game_model.game.manager.command import Command
from game_model.game.model import GameStatus
from services.session_service.domain.adapters import SessionStorage
from services.session_service.domain.models import SessionModel


class SessionEvents(Enum):
    PLAYER_CONNECTED = "PLAYER_CONNECTED"
    PLAYER_DISCONNECTED = "PLAYER_DISCONNECTED"
    STATE_CHANGED = "STATE_CHANGED"
    GAME_ENDED = "GAME_ENDED"


class CreateSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    def __call__(self, first_player_name: str, second_player_name: str) -> SessionModel:
        session = self._storage.create(first_player_name, second_player_name)
        session.disconnect(first_player_name)
        session.disconnect(second_player_name)
        self._storage.update(session)

        return session


class ConnectToSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    def __call__(self, player_name: str, session_id: int):
        session = self._storage.get(session_id)
        session.connect(player_name=player_name)
        self._storage.update(session)

        DomainEvents.raise_event(
            event_type=SessionEvents.PLAYER_CONNECTED,
            session_id=session_id,
            player_name=player_name
        )


class DisconnectFromSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    def __call__(self, player_name: str, session_id: int):
        session = self._storage.get(session_id)
        session.disconnect(player_name=player_name)
        self._storage.update(session)

        DomainEvents.raise_event(
            event_type=SessionEvents.PLAYER_DISCONNECTED,
            session_id=session_id,
            player_name=player_name
        )


class GetPlayer:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    def __call__(self, player_name: str, session_id: int):
        session = self._storage.get(session_id)
        return session.get_player(player_name)


class ExecuteCommand:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    def __call__(self, session_id: int, command: Command):
        session = self._storage.get(session_id)
        session.execute_command(command)
        self._storage.update(session)

        DomainEvents.raise_event(
            event_type=SessionEvents.STATE_CHANGED,
            session_id=session_id,
            changed_state=session.state
        )

        if session.state.status == GameStatus.SECOND_PLAYER_WIN:
            DomainEvents.raise_event(
                event_type=SessionEvents.GAME_ENDED,
                session_id=session.id,
                winner=session.get_players()[1]
            )
            self._storage.remove(session_id)

        if session.state.status == GameStatus.FIRST_PLAYER_WIN:
            DomainEvents.raise_event(
                event_type=SessionEvents.GAME_ENDED,
                session_id=session.id,
                winner=session.get_players()[0]
            )
            self._storage.remove(session_id)


class GetSession:
    _storage: SessionStorage

    def __init__(self, storage: SessionStorage):
        self._storage = storage

    async def __call__(self, session_id: int) -> SessionModel:
        return self._storage.get(session_id)
