from abc import ABC
from typing import Any, Awaitable, Callable, Dict

import aio_pika
import pydantic

from ..contract import ServiceEndpoint
from ..messages import RpcMessageGroup, RpcOnMessageGroup


class EndpointImplementation(pydantic.BaseModel):
    """
    pydantic модель, представляющая реализованную версию точки входа сервиса.

    Arguments:
        endpoint - информация о точке входа
        method - метод, реализующий соответствующий метод
    """

    endpoint: ServiceEndpoint
    method: Callable[..., Awaitable[Any]]


class BaseRpcService(ABC):
    """
    Базовый класс rpc сервиса. Поддерживает динамическое определение интерфейса сервиса

    Usage:
    ```
    class MyContract(RpcContract):
        @endpoint
        @abstractmethod
        def some_method(self, a: int, b: int):
            raise NotImplementedError()

    class MyImplementation(MyContract):
        def some_method(self, a: int, b: int):
            print(f'{a} + {b} = {a + b})

    implementation = MyImplementation()
    service = BaseRpcService(RpcMessageGroup())

    service.add_implementation('some_method', implementation)
    ```
    """

    _connect_properties = {"connection_name": "callee"}
    _messages: RpcMessageGroup
    _implementations: Dict[str, EndpointImplementation]

    _connection: aio_pika.abc.AbstractConnection
    _channel: aio_pika.abc.AbstractChannel
    _rpc: RpcOnMessageGroup

    def __init__(self, messages: RpcMessageGroup):
        """
        Инициализация сервиса

        :param messages: группа сообщений для сериализации десериализации
        """

        self._messages = messages
        self._implementations = dict()

        self._connection = None
        self._channel = None

    def add_implementation(self, endpoint: ServiceEndpoint, method: Callable[..., Awaitable[Any]]):
        """
        Добавляет реализацию точки входа к сервису

        :param endpoint: информация о точке входа
        :param method: метод, реализующий логику
        """

        self._implementations[endpoint.endpoint_name] = EndpointImplementation(
            endpoint=endpoint,
            method=method
        )

    async def _register_implementations(self):
        for endpoint_name, implementation in self._implementations.items():
            await self._rpc.register(endpoint_name, implementation.method, auto_delete=True)

    async def connect(self, credentials: str):
        """
        Подключение сервиса к rabbitmq серверу.

        :param credentials: данные для входа
        """

        self._connection = await aio_pika.connect_robust(credentials, client_properties=self._connect_properties)
        self._channel = await self._connection.channel()

        self._rpc = await RpcOnMessageGroup.create(self._channel)
        self._rpc.set_group(self._messages)
        await self._register_implementations()

    async def close(self):
        """
        Отключение сервиса от rabbitmq сервера. Обязательно вызывать при окончании работы программы.
        """

        await self._rpc.close()
        await self._channel.close()
        await self._connection.close()
