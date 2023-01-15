import json
import pydantic
from .base import PackedMessage, IRpcSerializable
from .exceptions import DeserializeMessageError, SerializeMessageError


class ResponseMessage(IRpcSerializable, pydantic.BaseModel):
    """
    Общий класс для сообщений - результатов работы
    """

    @classmethod
    def _get_message_type(cls) -> str:
        return f"response.{cls.__name__}"

    @classmethod
    def _can_be_deserialized(cls, message: PackedMessage) -> bool:
        return message.message_type == cls._get_message_type()

    @classmethod
    def serialize(cls, obj: "ResponseMessage") -> PackedMessage:
        if not isinstance(obj, cls):
            raise SerializeMessageError(message=obj, message_type=cls._get_message_type())

        return PackedMessage(
            message_type=cls._get_message_type(),
            data=obj.json().encode()
        )

    @classmethod
    def deserialize(cls, message: PackedMessage) -> "ResponseMessage":
        if not cls._can_be_deserialized(message):
            raise DeserializeMessageError(message, cls._get_message_type())

        args = json.loads(message.data.decode())

        try:
            return cls(**args)
        except pydantic.ValidationError:
            raise DeserializeMessageError(message, cls._get_message_type())
