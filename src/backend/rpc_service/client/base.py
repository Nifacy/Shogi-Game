from abc import ABC
from typing import Any, Awaitable, Callable, List, Dict

import aio_pika
import pydantic

from ..contract import ServiceEndpoint
from ..messages import RpcMessageGroup
from ..messages.rpc import RpcOnMessageGroup


class EndpointImplementation(pydantic.BaseModel):
    """
    Реализованная версия точки входа

    :param endpoint: информация о точке входа
    :param method: метод, обрабатывающий входящие запросы
    """

    endpoint: ServiceEndpoint
    method: Callable[..., Awaitable[Any]]


class BaseRpcClient:
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

    _connect_properties = {"connection_name": "caller"}
    _messages: RpcMessageGroup

    _connection: aio_pika.abc.AbstractConnection
    _channel: aio_pika.abc.AbstractChannel
    _rpc: RpcOnMessageGroup

    def __init__(self, messages: RpcMessageGroup):
        """
        Инициализация сервиса

        :param messages: группа сообщений для сериализации / десериализации
        """

        self._messages = messages
        self._connection = None
        self._channel = None

    async def call(self, endpoint_name: str, data: Any):
        """
        Базовый метод для отправки сообщений rpc сервису

        :param endpoint_name: название целевой точки входа сервиса
        :param data: аргументы, передаваемые обработчику
        :return: результат обработки запроса (указывает в контракте)
        """

        print(f'[RpcClient] Calling {endpoint_name}')
        response = await self._rpc.call(endpoint_name, kwargs=data)
        print(f'[RpcCLient] Received {response}')
        return response

    async def connect(self, credentials: str):
        """
        Подключение клиента к rabbitmq серверу

        :param credentials: данные для входа
        """

        self._connection = await aio_pika.connect_robust(credentials, client_properties=self._connect_properties)
        self._channel = await self._connection.channel()

        self._rpc = await RpcOnMessageGroup.create(self._channel)
        self._rpc.set_group(self._messages)

    async def close(self):
        """
        Отключение клиента от rabbitmq сервера. Обязательно вызывать после окончания работы программы
        """

        await self._rpc.close()
        await self._channel.close()
        await self._connection.close()
