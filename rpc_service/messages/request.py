import json
from typing import Any
import pydantic
from .base import IRpcSerializable, PackedMessage
from .exceptions import DeserializeMessageError, SerializeMessageError


class RequestMessage(IRpcSerializable, pydantic.BaseModel):
    @classmethod
    def _get_message_type(cls) -> str:
        return f"request.{cls.__name__}"

    @classmethod
    def _can_be_deserialized(cls, message: PackedMessage) -> bool:
        return message.message_type == cls._get_message_type()

    @classmethod
    def serialize(cls, obj: "RequestMessage") -> PackedMessage:
        if not isinstance(obj, cls):
            raise SerializeMessageError(message=obj, message_type=cls._get_message_type())

        serialized = obj.json().encode()
        return PackedMessage(message_type=cls._get_message_type(), data=serialized)

    @classmethod
    def deserialize(cls, message: PackedMessage) -> Any:
        if not cls._can_be_deserialized(message):
            raise DeserializeMessageError(message, cls._get_message_type())

        try:
            deserialized = dict(json.loads(message.data.decode()))
            return cls(**deserialized)
        except pydantic.ValidationError:
            raise DeserializeMessageError(packed_message=message, message_type=cls._get_message_type())
