from abc import ABC, abstractmethod
from .models import SessionModel


class NotExists(Exception):
    _tmp: str = "Session with id '{session_id}' not exists"
    session_id: int

    def __init__(self, session_id: int):
        super().__init__(self._tmp.format(session_id=session_id))
        self.session_id = session_id


class SessionStorage(ABC):
    @abstractmethod
    async def create(self, first_player_name: str, second_player_name: str) -> SessionModel:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, session_id: int) -> SessionModel:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, updated_data: SessionModel) -> SessionModel:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self, session_id: int):
        raise NotImplementedError()
