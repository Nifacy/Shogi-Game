from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from services.gateway_service.dependencies import get_current_user
from services.gateway_service.schemas import AccountInfo
from rpc_service import RpcClientBuilder
from contracts import account_service


users_router = APIRouter()
accounts_service_client = RpcClientBuilder.from_contract(account_service.Contract)


@users_router.on_event('startup')
async def open_connections():
    await accounts_service_client.connect('amqp://guest:guest@localhost')


@users_router.on_event('shutdown')
async def close_connections():
    await accounts_service_client.close()


@users_router.get('/me')
async def get_current_user_account_info(current_user: AccountInfo = Depends(get_current_user)):
    return current_user


@users_router.get('/{username}')
async def get_user_b_username(username: str) -> AccountInfo:
    try:
        account = await accounts_service_client.get_account(username=username)
        return AccountInfo(username=account.username, rating=account.rating)
    except account_service.NotExists as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
