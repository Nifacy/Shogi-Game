import json
from typing import Any
from .base import IRpcSerializable, PackedMessage
from .exceptions import SerializeMessageError, DeserializeMessageError


class SuccessMessage(IRpcSerializable):
    @classmethod
    def _get_message_type(cls) -> str:
        return f'response.{cls.__name__}'

    @classmethod
    def serialize(cls, obj: Any) -> PackedMessage:
        if obj is not None:
            raise SerializeMessageError(message=obj, message_type=cls._get_message_type())

        data = {'result': 'success'}
        return PackedMessage(message_type=cls._get_message_type(), data=json.dumps(data).encode())

    @classmethod
    def deserialize(cls, message: PackedMessage) -> Any:
        if message.message_type != cls._get_message_type():
            raise DeserializeMessageError(packed_message=message, message_type=cls._get_message_type())

        return cls()
