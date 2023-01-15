from abc import ABC, abstractmethod

from .models import AccountModel


class AlreadyExists(Exception):
    _tmp: str = "Account with username '{username}' already exists"
    _username: str

    def __init__(self, username: str):
        super().__init__(self._tmp.format(username=username))
        self._username = username

    @property
    def username(self) -> str:
        return self._username


class NotExists(Exception):
    _tmp: str = "Account with username '{username}' not exists"
    _username: str

    def __init__(self, username: str):
        super().__init__(self._tmp.format(username=username))

    @property
    def username(self) -> str:
        return self._username


class AccountStorage(ABC):
    @abstractmethod
    async def create(self, username: str) -> AccountModel:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, username: str) -> AccountModel:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, updated_data: AccountModel) -> AccountModel:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self, username: str):
        raise NotImplementedError()
