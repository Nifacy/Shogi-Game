from services.auth_service.domain import adapters, models


class RegisterUser:
    _storage: adapters.CredentialsStorage

    def __init__(self, storage: adapters.CredentialsStorage):
        self._storage = storage

    async def __call__(self, credentials: models.CredentialsModel) -> models.CredentialsModel:
        return await self._storage.create_record(credentials)


class AuthorizeUser:
    _method: adapters.ValidateMethod

    def __init__(self, method: adapters.ValidateMethod):
        self._method = method

    async def __call__(self, auth_data: models.AuthorizationData) -> models.AuthenticationData:
        return await self._method.authorize(auth_data)


class AuthenticateUser:
    _method: adapters.ValidateMethod

    def __init__(self, method: adapters.ValidateMethod):
        self._method = method

    async def __call__(self, auth_data: models.AuthenticationData) -> models.CredentialsModel:
        return await self._method.validate(auth_data)
