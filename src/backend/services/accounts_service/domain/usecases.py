from .adapters import AccountStorage
from .models import AccountModel


class CreateAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    async def __call__(self, username: str) -> AccountModel:
        return await self._storage.create(username)


class RemoveAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    async def __call__(self, username: str):
        await self._storage.remove(username)


class GetAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    async def __call__(self, username: str) -> AccountModel:
        return await self._storage.get(username)


class UpdateAccount:
    _storage: AccountStorage

    def __init__(self, storage: AccountStorage):
        self._storage = storage

    async def __call__(self, updated: AccountModel) -> AccountModel:
        return await self._storage.update(updated)
