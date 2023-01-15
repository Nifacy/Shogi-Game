from contracts import auth_service
from services.auth_service import domain, infrastructure
from services.auth_service.domain import adapters


class Implementation(auth_service.Contract):
    def __init__(self, database: adapters.CredentialsStorage, validate_method: adapters.ValidateMethod):
        self._database = database
        self._validate_method = validate_method

    async def register_user(self, login: str, password: str) -> auth_service.Token:
        try:
            credentials = domain.CredentialsModel(login=login, password=password)
            await domain.RegisterUser(self._database)(credentials)

        except domain.adapters.AlreadyRegistered:
            raise auth_service.UsernameTaken(username=login)

        auth_data = infrastructure.Authorize(login=login, password=password)
        token: infrastructure.Token = await domain.AuthorizeUser(self._validate_method)(auth_data)

        return auth_service.Token(access_token=token.token, token_type='bearer')

    async def generate_access_token(self, login: str, password: str) -> auth_service.Token:
        try:
            auth_data = infrastructure.Authorize(login=login, password=password)
            token: infrastructure.Token = await domain.AuthorizeUser(self._validate_method)(auth_data)

        except domain.adapters.InvalidAuthorizationData:
            raise auth_service.InvalidCredentials()

        return auth_service.Token(access_token=token.token, token_type='bearer')

    async def authenticate(self, token: str) -> auth_service.TokenData:
        try:
            credentials = await domain.AuthenticateUser(self._validate_method)(infrastructure.Token(token=token))

        except domain.adapters.InvalidAuthenticationData:
            raise auth_service.InvalidToken(token=token)

        return auth_service.TokenData(username=credentials.login)
