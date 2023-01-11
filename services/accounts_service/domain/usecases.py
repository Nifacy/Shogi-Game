from .adapters import AccountStorage
from .models import AccountModel


class CreateAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    def __call__(self, username: str) -> AccountModel:
        return self._storage.create(username)


class RemoveAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    def __call__(self, username: str):
        self._storage.remove(username)


class GetAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    def __call__(self, username: str) -> AccountModel:
        return self._storage.get(username)


class UpdateAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    def __call__(self, updated: AccountModel) -> AccountModel:
        return self._storage.update(updated)
