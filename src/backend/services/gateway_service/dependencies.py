from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from contracts import account_service, auth_service
from rpc_service import RpcClientBuilder
from services.gateway_service import schemas
from services.gateway_service.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


class AuthDependency:
    def __init__(self):
        self._accounts_service_client = RpcClientBuilder.from_contract(account_service.Contract)
        self._auth_service_client = RpcClientBuilder.from_contract(auth_service.Contract)
        self._connected = False

    async def _connect_clients(self):
        await self._accounts_service_client.connect(settings.amqp_dsn)
        await self._auth_service_client.connect(settings.amqp_dsn)

    async def __call__(self, token: str = Depends(oauth2_scheme)) -> schemas.AccountInfo:
        if not self._connected:
            await self._connect_clients()
            self._connected = True

        try:
            decoded = await self._auth_service_client.authenticate(token=token)
            print(decoded)
            account = await self._accounts_service_client.get_account(username=decoded.username)
            return schemas.AccountInfo(username=account.username, rating=account.rating)
        except (auth_service.InvalidToken, account_service.NotExists):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


get_current_user = AuthDependency()
