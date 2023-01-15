from dataclasses import dataclass
from rpc_service import ErrorResponse, RpcMessageGroup, ResponseMessage, RpcContract, endpoint


messages = RpcMessageGroup()


@messages.add_message_type
@dataclass
class UsernameTaken(ErrorResponse):
    username: str
    _message: str = 'Username {username!r} taken'


@messages.add_message_type
@dataclass
class InvalidCredentials(ErrorResponse):
    _message: str = 'Invalid username or password'


@messages.add_message_type
@dataclass
class InvalidToken(ErrorResponse):
    token: str
    _message: str = 'Token {token!r} invalid'


@messages.add_message_type
class Token(ResponseMessage):
    access_token: str
    token_type: str


@messages.add_message_type
class TokenData(ResponseMessage):
    username: str


class Contract(RpcContract):
    __service__ = 'auth_service'
    __messages__ = messages

    @endpoint
    async def register_user(self, login: str, password: str) -> Token:
        """
        Регистрация пользователя

        :param login: логин пользователя
        :param password: пароль пользователя
        :return: сгенерированный токен доступа
        :raise UsernameTaken: пользователь с указанным логином уже зарегестрирован
        """
        raise NotImplementedError()

    @endpoint
    async def generate_access_token(self, login: str, password: str) -> Token:
        """
        Авторизация пользователя

        :param login: логин пользователя
        :param password: пароль пользователя
        :return: сгенерированный токен доступа
        :raise InvalidCredentials: переданы неверные данные для входа
        """
        raise NotImplementedError()

    @endpoint
    async def authenticate(self, token: str) -> TokenData:
        """
        Аутентификация пользователя по токену доступа

        :param token: токен доступа
        :return: данные, хранящиеся в токене
        :raise InvalidToken: отправленный токен неверный
        """
        raise NotImplementedError()
