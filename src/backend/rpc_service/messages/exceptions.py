from typing import Any
from .base import PackedMessage


class DeserializeMessageError(Exception):
    """
    Исключение, вызываемое в момент, когда переданное упакованное сообщение
    не может быть десериализовано в объект текущего типа сообщений

    Arguments:
        packed_message - переданное упакованное сообщение
        message_type - тип сообщения, в который происходила десериализация
    """

    _message: str = "Packed message {packed_message} can't be serialized to '{message_type}'"
    packed_message: PackedMessage
    message_type: str

    def __init__(self, packed_message: PackedMessage, message_type: str):
        super().__init__(self._message.format(packed_message=packed_message, message_type=message_type))


class SerializeMessageError(Exception):
    """
    Исключение, вызываемое в момент, когда переданное упакованное сообщение
    не может быть десериализовано в объект текущего типа сообщений (обычно происходит
    при передаче объекта не соответствующего типа)

    Arguments:
        message - сообщение, который пытались сериализовать
        message_type - предполагаемый тип сообщения
    """

    _message: str = "Message {message} can't be serialized with '{message_type}'"
    packed_message: Any
    message_type: str

    def __init__(self, message: Any, message_type: str):
        super().__init__(self._message.format(message=message, message_type=message_type))