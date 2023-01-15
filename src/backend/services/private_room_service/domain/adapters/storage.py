from abc import abstractmethod, ABC
from .. import models


class NotExists(Exception):
    """
    Исключение, вызываемое хранилищем приватных комнат, в момент,
    когда требуемой приватной комнаты не существует

    Arguments:
        connection_key - ключ подключения, по которому производился поиск
    """

    connection_key: models.ConnectionKey
    __message: str = 'Private room with connection key {connection_key!r} not exists'

    def __init__(self, connection_key: models.ConnectionKey):
        super().__init__(self.__message.format(connection_key=connection_key))
        self.connection_key = connection_key


class AlreadyExists(Exception):
    """
    Исключение, вызываемое хранилищем приватных комнат, в момент, когда
    комната с текущим ключом подключения уже существует

    Argument:
        connection_key - ключ подключения, по которому создавалась комната
    """

    connection_key: models.ConnectionKey
    __message: str = 'Private room with connection key {connection_key!r} already exists'

    def __init__(self, connection_key: models.ConnectionKey):
        super().__init__(self.__message.format(connection_key=connection_key))
        self.connection_key = connection_key


class PrivateRoomStorage(ABC):
    """
    Адаптер к хранилищу приватных комнат.
    """

    @abstractmethod
    async def create_room(self, connection_key: models.ConnectionKey) -> models.PrivateRoom:
        """
        Создать новую приватную комнату с указанным ключом подключения

        :param connection_key:
        :return: созданная приватная комната
        :raise AlreadyExists: приватная комната с таким ключом подключения существует
        """
        raise NotImplementedError()

    @abstractmethod
    async def remove_room(self, connection_key: models.ConnectionKey):
        """
        Удаляет приватную комнату с указанным ключом подключения

        :param connection_key: ключ подключения, соответствующий удаляемой комнате
        :raise NotExists: комната с таким ключом подключения не существует
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_room(self, updated_data: models.PrivateRoom) -> models.PrivateRoom:
        """
        Обновляет информацию о приватной комнате

        :param updated_data: новая информация о приватной комнате
        :return: обновленная информация из хранилища
        :raise NotExists: приватная комната не была до этого создана
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_room(self, connection_key: models.ConnectionKey) -> models.PrivateRoom:
        """
        Возвращает информацию о приватной комнате, ключ
        подключения которой соответствует переданному

        :param connection_key: ключ подключения, по которому идет поиск комнаты
        :return: найденная информация о приватной комнате
        :raise NotExists: приватная комната не была до этого создана
        """
        raise NotImplementedError()
