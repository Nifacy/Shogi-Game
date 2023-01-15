import dataclasses
import json

import pydantic.json

from .base import IRpcSerializable, PackedMessage
from .exceptions import DeserializeMessageError, SerializeMessageError


@dataclasses.dataclass
class ErrorResponse(IRpcSerializable, Exception):
    """
    Общий класс для сообщений - исключений, отправляемых сервисом в моменты,
    когда произошла ошибка во время исполнения

    Arguments:
        _message (optional) - текст сообщения ошибки. Является format строкой, куда вставляются значения
        полей текущего объекта

    Usage:
    ```
    @dataclass
    class MyCustomError(ErrorResponse):
        username: str
        age: int
        _message: str = 'User {username} has age {age}'
    ```
    """

    def __post_init__(self):
        msg = getattr(self, '_message', 'ErrorResponse')
        msg = msg.format(**dataclasses.asdict(self))
        super(Exception, self).__init__(msg)

    @classmethod
    def _get_message_type(cls):
        return f"error.{cls.__name__}"

    @classmethod
    def serialize(cls, obj: "ErrorResponse") -> PackedMessage:
        if not isinstance(obj, cls):
            raise SerializeMessageError(message=obj, message_type=cls._get_message_type())

        serialized = json.dumps(obj, default=pydantic.json.pydantic_encoder)
        serialized = dict(json.loads(serialized))

        if "_message" in serialized:
            serialized.pop("_message")

        return PackedMessage(
            message_type=cls._get_message_type(),
            data=json.dumps(serialized).encode()
        )

    @classmethod
    def deserialize(cls, message: PackedMessage) -> "ErrorResponse":
        if not cls._can_be_deserialized(message):
            raise DeserializeMessageError(message, cls._get_message_type())

        args = json.loads(message.data.decode())
        try:
            return cls(**args)
        except TypeError:
            raise DeserializeMessageError(message, cls._get_message_type())

    @classmethod
    def _can_be_deserialized(cls, message: PackedMessage) -> bool:
        return message.message_type == cls._get_message_type()
