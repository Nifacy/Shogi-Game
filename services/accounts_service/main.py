# Response Models
import asyncio

from pydantic import BaseModel

from rpc_service.handler import ResponseError
from rpc_service.service import RPCService
from services.accounts_service.domain.adapters import AlreadyExists, NotExists
from services.accounts_service.domain.usecases import *
from services.accounts_service.infrastracture import DefaultAccountDatabase


class AccountInfo(BaseModel):
    username: str
    rating: int


class ResponseMessage(BaseModel):
    message_type: str
    detail: str


# Variables

db = DefaultAccountDatabase()

# Endpoints


async def create_user(username: str) -> AccountInfo:
    try:
        account = CreateAccount(db)(username)
    except AlreadyExists as e:
        raise ResponseError(error_type="already_exists", detail=f"Account with name '{username}' already exists")

    response = AccountInfo(username=account.username, rating=account.rating)
    return response


async def get_user(username: str) -> AccountInfo:
    try:
        account = GetAccount(db)(username)
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=f"Account with username '{username}' doesn't exist")

    response = AccountInfo(username=account.username, rating=account.rating)
    return response


async def update_user(updated_data: AccountInfo) -> AccountInfo:
    try:
        account = AccountModel(**updated_data.dict())
        updated_account = UpdateAccount(db)(account)
    except NotExists as e:
        raise ResponseError(
            error_type="not_exists",
            detail=f"Account with username '{updated_data.username}' doesn't exist")

    response = AccountInfo(username=updated_account.username, rating=updated_account.rating)
    return response


async def remove_user(username: str):
    try:
        RemoveAccount(db)(username)
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=f"Account with username '{username}' doesn't exist")

    response = ResponseMessage(message_type="success", detail="Successful")
    return response


# Service

service = RPCService("accounts_service", "amqp://guest:guest@localhost")
service.bind("create", create_user)
service.bind("get", get_user)
service.bind("update", update_user)
service.bind("remove", remove_user)


async def main():
    await service.run()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
