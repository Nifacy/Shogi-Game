from contracts import account_service
from services.accounts_service import domain
from services.accounts_service.domain import adapters


class Implementation(account_service.Contract):
    def __init__(self, storage: adapters.AccountStorage):
        self._storage = storage

    async def create_account(self, username: str) -> account_service.AccountInfo:
        try:
            account = await domain.CreateAccount(self._storage)(username)

        except domain.AlreadyExists:
            raise account_service.AlreadyExists(username=username)

        response = account_service.AccountInfo(username=account.username, rating=account.rating)
        return response

    async def update_account(self, updated_data: account_service.AccountInfo) -> account_service.AccountInfo:
        try:
            account = domain.AccountModel(**updated_data.dict())
            updated_account = await domain.UpdateAccount(self._storage)(account)

        except domain.NotExists:
            raise account_service.NotExists(username=updated_data.username)

        response = account_service.AccountInfo(username=updated_account.username, rating=updated_account.rating)
        return response

    async def get_account(self, username: str) -> account_service.AccountInfo:
        try:
            account = await domain.GetAccount(self._storage)(username)

        except domain.NotExists:
            raise account_service.NotExists(username=username)

        response = account_service.AccountInfo(username=account.username, rating=account.rating)
        return response

    async def delete_account(self, username: str):
        try:
            await domain.RemoveAccount(self._storage)(username)

        except domain.NotExists:
            raise account_service.NotExists(username=username)
