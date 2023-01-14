from dataclasses import dataclass
from rpc_service import ErrorResponse, RpcMessageGroup, ResponseMessage, RpcContract, endpoint


messages = RpcMessageGroup()


@messages.add_message_type
class AccountInfo(ResponseMessage):
    username: str
    rating: int


@messages.add_message_type
@dataclass
class AlreadyExists(ErrorResponse):
    username: str
    _message: str = 'Username {username!r} taken'


@messages.add_message_type
@dataclass
class NotExists(ErrorResponse):
    username: str
    _message: str = 'Account with username {username!r} not exists'


class Contract(RpcContract):
    __service__ = 'accounts_service'
    __messages__ = messages

    @endpoint
    async def create_account(self, username: str) -> AccountInfo:
        """
        Создает аккаунт с указанным именем

        :param username: имя аккаунта
        :raise AlreadyExists: если указанное имя уже занято
        """
        raise NotImplementedError()

    @endpoint
    async def update_account(self, updated_data: AccountInfo) -> AccountInfo:
        """
        Обновляет информацию об аккаунте

        :raise NotExists: если аккаунта с таким именем не существует
        :param updated_data: обновленная информация
        :return: результат обновления информации
        """
        raise NotImplementedError()

    @endpoint
    async def get_account(self, username: str) -> AccountInfo:
        """
        Получение аккаунта с указанным именем

        :raise NotExists: если аккаунта с таким именем не существует
        :param username: имя аккаунта, которого ищем
        """
        raise NotImplementedError()

    @endpoint
    async def delete_account(self, username: str):
        """
        Удаление аккаунта с указанным именем

        :raise NotExists: если аккаунта с таким именем нет
        :param username: имя аккаунта, который удаляем
        """
        raise NotImplementedError()
