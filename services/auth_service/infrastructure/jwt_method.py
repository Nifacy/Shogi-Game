from dataclasses import dataclass

import jwt

from ..domain import models
from ..domain import adapters
from ..domain.models import AuthenticationData, AuthorizationData, Login, Password


@dataclass(frozen=True)
class Token(AuthenticationData):
    token: str


@dataclass(frozen=True)
class Authorize(AuthorizationData):
    login: Login
    password: Password


@dataclass(frozen=True)
class JWTSecrets:
    key: str
    algorithm: str


class JWTMethod(adapters.ValidateMethod):
    """
    Метод аутентификации / авторизации пользователей на основе JWT токенов
    """

    _storage: adapters.CredentialsStorage
    _secrets: JWTSecrets

    def __init__(self, storage: adapters.CredentialsStorage, secrets: JWTSecrets):
        self._storage = storage
        self._secrets = secrets

    async def validate(self, data: Token) -> models.CredentialsModel:
        try:
            decoded = jwt.decode(data.token, self._secrets.key, algorithms=[self._secrets.algorithm])
            return await self._storage.get_record(decoded.get('login'))

        except (jwt.DecodeError, TypeError):
            raise adapters.InvalidAuthenticationData(data)

    async def authorize(self, data: Authorize) -> Token:
        try:
            check_credentials = models.CredentialsModel(login=data.login, password=data.password)
            await self._storage.validate(check_credentials)
            token = jwt.encode({'login': data.login}, self._secrets.key, algorithm=self._secrets.algorithm)
            return Token(token=token)

        except adapters.NotExists:
            raise adapters.InvalidAuthorizationData(data)
