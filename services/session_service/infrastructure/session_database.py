from copy import deepcopy

from services.session_service.domain.adapters import SessionStorage, NotExists
from services.session_service.domain.factories import state_factory
from services.session_service.domain.models import SessionModel, PlayerConnectionState, PlayerModel


def session_factory(session_id: int, first_player_name: str, second_player_name: str) -> SessionModel:
    first_player = PlayerModel(_name=first_player_name)
    second_player = PlayerModel(_name=second_player_name)

    session = SessionModel(
        _session_id=session_id,
        _players=(first_player, second_player),
        _player_connections={
            first_player.name: PlayerConnectionState.DISCONNECTED,
            second_player.name: PlayerConnectionState.DISCONNECTED
        },
        _state=state_factory(first_player=first_player, second_player=second_player))

    return session


class DefaultSessionDatabase(SessionStorage):
    _db: dict
    _last_id: int

    def __init__(self):
        self._last_id = 0
        self._db = dict()

    def _generate_id(self):
        self._last_id += 1
        return self._last_id

    def create(self, first_player_name: str, second_player_name: str) -> SessionModel:
        new_session = session_factory(self._generate_id(), first_player_name, second_player_name)
        self._db[new_session.id] = new_session
        return new_session

    def get(self, session_id: int) -> SessionModel:
        if session_id not in self._db:
            raise NotExists(session_id=session_id)

        return self._db[session_id]

    def update(self, updated_data: SessionModel) -> SessionModel:
        if updated_data.id not in self._db:
            raise NotExists(session_id=updated_data.id)

        self._db[updated_data.id] = updated_data
        return updated_data

    def remove(self, session_id: int):
        if session_id not in self._db:
            raise NotExists(session_id=session_id)

        del self._db[session_id]
