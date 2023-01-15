import asyncio
import json
from typing import Awaitable, Callable

from aio_pika import connect, Message
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractExchange, ExchangeType


EventObserver = Callable[[dict], Awaitable[None]]


class AmqpEventPublisher:
    _event_name: str

    _connection: AbstractConnection
    _channel: AbstractChannel
    _exchange: AbstractExchange
    _loop: asyncio.AbstractEventLoop

    def __init__(self, event_name: str):
        self._event_name = event_name

    async def connect(self, credentials: str):
        self._loop = asyncio.get_running_loop()
        self._connection = await connect(credentials, loop=self._loop)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(self._event_name, ExchangeType.FANOUT)

    async def notify(self, message: dict):
        print(f"Publisher: Notify all '{self._event_name}' subscribers")
        await self._exchange.publish(Message(body=json.dumps(message).encode()), routing_key='')

    async def close(self):
        await self._channel.close()
        await self._connection.close()
