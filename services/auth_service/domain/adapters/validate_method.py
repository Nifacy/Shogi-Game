from abc import ABC, abstractmethod
from .. import models


class InvalidAuthenticationData(Exception):
    """
    Исключение, вызываемое методом проверки запрос для входа
    когда данные для аутентификации неверные

    Arguments:
        data - данные для аутентификации, которые пришли
    """

    data: models.AuthenticationData
    __message: str = 'Authentication data {data!r} invalid'

    def __init__(self, data: models.AuthenticationData):
        super().__init__(self.__message.format(data=data))
        self.data = data


class InvalidAuthorizationData(Exception):
    """
    Исключение, вызываемое методом проверки запросов для
    входа когда данные для авторизации неверные

    Arguments:
        data - данные для авторизации, которые пришли
    """

    data: models.AuthorizationData
    __message: str = 'Authorization data {data!r} invalid'

    def __init__(self, data: models.AuthorizationData):
        super().__init__(self.__message.format(data=data))
        self.data = data


class ValidateMethod(ABC):
    """
    Адаптер к методу проверки запросов для авторизации / аутентификации
    """

    @abstractmethod
    async def validate(self, data: models.AuthenticationData) -> models.CredentialsModel:
        """
        Метод для аутентификации пользователя

        :param data: данные для аутентификации
        :return: данные для входа. Возвращаются в случае, если аутентификация прошла успешна
        :raise InvalidAuthenticationData: не удалось аутентифицировать пользователя
        """
        raise NotImplementedError()

    @abstractmethod
    async def authorize(self, data: models.AuthorizationData) -> models.AuthenticationData:
        """
        Метод для авторизации пользователя

        :param data: данные для авторизации
        :return: данные для аутентификации. Возвращаются в случае, если авторизация прошла успешно
        :raise InvalidAuthenticationData: не удалось авторизовать пользователя
        """
        raise NotImplementedError()
