from abc import ABC, abstractmethod
from typing import Any

import pydantic


class PackedMessage(pydantic.BaseModel):
    """
    Общий объект для представления упакованных сообщений.

    Attributes:
        message_type - тип сообщения. Указывается для сериализации / десериализации сообщений
        data - данные, передаваемые через сообщение.
    """
    message_type: str
    data: bytes


class IRpcSerializable(ABC):
    """
    Интерфейс типов сообщений. Содержат методы по сериализации / десериализации
    """

    @classmethod
    @abstractmethod
    def serialize(cls, obj: Any) -> PackedMessage:
        """
        Метод сериализации сообщения.
        :throws SerializeMessageException: если не может быть сериализовано
        :param obj: сериализуемое сообщение
        :return: упакованное сообщение
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def deserialize(cls, message: PackedMessage) -> Any:
        """
        :raise DeserializeMessageError: если не может быть десериализовано
        :param message: десериализуемое упакованное сообщение
        :return: десериализованное сообщение
        """
        raise NotImplementedError()
