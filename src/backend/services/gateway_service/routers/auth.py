from fastapi import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from contracts import auth_service, account_service
from rpc_service import RpcClientBuilder
from services.gateway_service import schemas

from services.gateway_service.settings import settings

auth_router = APIRouter()
auth_service_client = RpcClientBuilder.from_contract(auth_service.Contract)
account_service_client = RpcClientBuilder.from_contract(account_service.Contract)


@auth_router.on_event('startup')
async def open_connections():
    await auth_service_client.connect(settings.amqp_dsn)
    await account_service_client.connect(settings.amqp_dsn)


@auth_router.on_event('shutdown')
async def close_connection():
    await auth_service_client.close()
    await account_service_client.close()


@auth_router.post('/register')
async def register_user(credentials: schemas.Registration) -> schemas.Token:
    try:
        token = await auth_service_client.register_user(login=credentials.username, password=credentials.password)
        await account_service_client.create_account(username=credentials.username)
    except auth_service.UsernameTaken:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username taken')

    return schemas.Token(**token.dict())


@auth_router.post('/login')
async def authorize_user(credentials: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    try:
        token = await auth_service_client.generate_access_token(login=credentials.username, password=credentials.password)
        return schemas.Token(**token.dict())
    except auth_service.InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong password or username')
