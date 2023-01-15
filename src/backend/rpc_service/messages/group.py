from typing import List, Type, Any, TypeVar
from .base import IRpcSerializable, PackedMessage
from .exceptions import SerializeMessageError, DeserializeMessageError


_MessageType = TypeVar('_MessageType', bound=Type[IRpcSerializable])


class RpcMessageGroup:
    """
    Реализация паттерна 'Компоновщик'. Позволяет сгруппировать несколько типов сообщений
    и работать как с одним целым.

    (Не имплементирует интерфейс IRpcSerializable в связи с возникающими трудностями при проектировании)
    """

    __message_types: List[Type[IRpcSerializable]]

    def __init__(self):
        self.__message_types = list()

    def __repr__(self):
        message_types = [repr(message_type) for message_type in self.__message_types]
        return 'RpcMessageGroup({})'.format(', '.join(message_types))

    def add_message_type(self, message_type: _MessageType) -> _MessageType:
        """
        Добавляет текущий тип сообщений к группе

        :param message_type: добавляемый тип сообщений
        :return:
        """

        if message_type not in self.__message_types:
            self.__message_types.append(message_type)

        return message_type

    def serialize(self, obj: Any) -> PackedMessage:
        for message_type in self.__message_types:
            try:
                return message_type.serialize(obj)
            except SerializeMessageError:
                pass

        raise SerializeMessageError(obj, repr(self))

    def deserialize(self, message: PackedMessage) -> Any:
        for message_type in self.__message_types:
            try:
                return message_type.deserialize(message)
            except DeserializeMessageError:
                pass

        raise DeserializeMessageError(message, repr(self))
