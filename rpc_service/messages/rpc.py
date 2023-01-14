import json
from typing import Any
import aio_pika

from .exceptions import SerializeMessageError
from .request import RequestMessage
from .errors import ErrorResponse
from .base import PackedMessage
from .group import RpcMessageGroup


class RpcOnMessageGroup(aio_pika.patterns.RPC):
    """
    Шаблон RPC объекта, поддерживающего сериализацию / десериализацию указанной группы сообщений.
    """

    _group: RpcMessageGroup
    CONTENT_TYPE = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._group = None

    def set_group(self, group: RpcMessageGroup):
        """
        Присваивает текущему группу сообщений, на основе которой будет происходить сериализация сообщений.
        Обязательно вызывать перед использованием и после инициализации.

        :param group: группа сообщений, с которой будет работать RPC объект
        """

        self._group = group

    def serialize(self, data: Any) -> bytes:
        packed = self._group.serialize(data)
        print(f'[RPC] Serialize {data} -> {repr(packed)}')
        return packed.json().encode()

    def deserialize(self, message: bytes) -> Any:
        packed = PackedMessage(**json.loads(message.decode()))
        deserialized = self._group.deserialize(packed)

        if isinstance(deserialized, RequestMessage):
            deserialized = dict(deserialized)

        if isinstance(deserialized, ErrorResponse):
            raise deserialized

        print(f'[RPC] Deserialize {repr(packed)} -> {deserialized}')
        return deserialized

    def serialize_exception(self, exception: Exception) -> Any:
        try:
            self._group.serialize(exception)
            return exception
        except SerializeMessageError:
            raise exception
