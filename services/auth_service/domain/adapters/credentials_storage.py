from abc import ABC, abstractmethod
from services.auth_service.domain import models


class NotExists(Exception):
    """
    Исключение, выбрасываемое хранилищем в момент, когда поиск
    записи оказался неудачным

    Arguments:
        login - логин, по которому искалась запись
    """
    login: models.Login
    __message: str = 'Record for user with login {login!r} not exists'

    def __init__(self, login: models.Login):
        super().__init__(self.__message.format(login=login))


class AlreadyRegistered(Exception):
    """
    Исключение, выбрасываемое хранилищем в момент, когда добавляемый
    пользователь уже был создан

    Arguments:
        credentials - данные для входа, которые нужно было добавить
    """
    credentials: models.CredentialsModel
    __message: str = 'Credentials for user {login!r} already exist'

    def __init__(self, credentials: models.CredentialsModel):
        super().__init__(self.__message.format(login=credentials.login))
        self.credentials = credentials


class CredentialsStorage(ABC):
    """
    Адаптер к хранилищу данных для входа пользователей
    """

    @abstractmethod
    async def create_record(self, credentials: models.CredentialsModel) -> models.CredentialsModel:
        """
        Создает запись с данными для входа пользователя в хранилище

        :raise AlreadyRegistered: пользователь с таким же логином уже зарегестрирован
        :param credentials: данные для входа пользователя
        :return: данные, которые сохранились
        """
        raise NotImplementedError()

    @abstractmethod
    async def remove_record(self, login: str):
        """
        Удаляет запись с данными для входа из хранилища
        :param login: логин пользователя, данные которого удаляем
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_record(self, login: str) -> models.CredentialsModel:
        """
        Возвращает данные для входа пользователя по его логину
        :param login: логин пользователя
        :return: соответствующие данные для входа
        """
        raise NotImplementedError()

    @abstractmethod
    async def validate(self, credentials: models.CredentialsModel):
        """
        Проверяет наличие переданных данных для входа в хранилище. В случае, если
        было проверено успешно, ничего не возвращается.

        :param credentials: данные для входа, которые проверяем
        :raise NotExists: если не было найдено такой записи
        """
        raise NotImplementedError()

