from abc import ABC
from dataclasses import dataclass
from typing import NewType


Login = NewType('Login', str)
Password = NewType('Password', str)


@dataclass(frozen=True)
class CredentialsModel:
    """
    Бизнес модель данных для входа пользователя

    Arguments:
        username - имя пользователя
        hashed_password - зашифрованный пароль
    """

    login: Login
    password: Password


class AuthenticationData(ABC):
    """
    Модель запроса, посылаемого для аутентификации пользователя. Конкретная реализация
    уточняется в инфраструктуре на основе метода аутентификации
    """
    pass


class AuthorizationData(ABC):
    """
    Модель запроса, посылаемого для авторизации пользователя. Конкретная реализация
    уточняется в инфраструктуре на основе метода авторизации
    """
    pass
