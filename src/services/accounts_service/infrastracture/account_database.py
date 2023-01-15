from pydantic import BaseModel

from services.accounts_service.domain.adapters import AccountStorage, AlreadyExists, NotExists
from services.accounts_service.domain.models import AccountModel


class AccountDBModel(BaseModel):
    username: str
    rating: int


class DefaultAccountDatabase(AccountStorage):
    _db: dict

    def __init__(self):
        self._db = dict()

    def create(self, username: str) -> AccountModel:
        if username in self._db:
            raise AlreadyExists(username)
        record = AccountDBModel(username=username, rating=0)
        domain_model = AccountModel(record.username, record.rating)
        self._db[username] = record
        return domain_model

    def get(self, username: str) -> AccountModel:
        if username not in self._db:
            raise NotExists(username)
        record = self._db[username]
        return AccountModel(username=record.username, rating=record.rating)

    def update(self, updated_data: AccountModel) -> AccountModel:
        if updated_data.username not in self._db:
            raise NotExists(updated_data.username)
        record = AccountDBModel(username=updated_data.username, rating=updated_data.rating)
        self._db[record.username] = record
        return updated_data

    def remove(self, username: str):
        if username not in self._db:
            raise NotExists(username)
        del self._db[username]
