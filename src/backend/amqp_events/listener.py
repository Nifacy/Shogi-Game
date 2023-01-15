import asyncio
import json
import logging
from asyncio import Task
from typing import List, Awaitable, Callable

from aio_pika import connect
from aio_pika.abc import *


EventObserver = Callable[[dict], Awaitable[None]]


class AmqpEventListener:
    _event_name: str
    _observers: List[EventObserver]
    _running_tasks: List[Task]

    _connection: AbstractConnection
    _channel: AbstractChannel
    _exchange: AbstractExchange
    _queue: AbstractQueue
    _loop: asyncio.AbstractEventLoop

    def __init__(self, event_name: str):
        self._event_name = event_name
        self._observers = list()
        self._running_tasks = list()

    async def _notify(self, message: AbstractIncomingMessage):
        async with message.process():
            decoded_message = json.loads(message.body.decode())

            print(f"AMQPListener({self._event_name}): Sending to observers...!")

            for observer in self._observers:
                task = asyncio.create_task(observer(decoded_message))
                task.add_done_callback(self._remove_task)
                self._running_tasks.append(task)

    def _remove_task(self, task: Task):
        if task in self._running_tasks:
            self._running_tasks.remove(task)

    def attach(self, observer: EventObserver):
        if observer not in self._observers:
            print(f"AMQPListener({self._event_name!r}) : Attached {observer}")
            self._observers.append(observer)

    def detach(self, observer: EventObserver):
        if observer in self._observers:
            print(f"AMQPListener({self._event_name!r}) : Detached {observer}")
            self._observers.remove(observer)

    async def connect(self, credentials: str):
        print(f"AMQPListener({self._event_name!r}): Connecting...")

        self._loop = asyncio.get_running_loop()
        self._connection = await connect(credentials, loop=self._loop)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(self._event_name, ExchangeType.FANOUT)
        self._queue = await self._channel.declare_queue(exclusive=True)

        await self._queue.bind(self._exchange)
        await self._queue.consume(self._notify)

    async def close(self):
        await self._queue.unbind(self._exchange)
        await self._queue.close_callbacks()
        await self._channel.close()
        await self._connection.close()
