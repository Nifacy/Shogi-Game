import asyncio
from collections import defaultdict
from typing import List, Dict

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange

from rpc_service.handler import RequestHandler, HandleFunction


class RPCService:
    _service_name: str
    _connection_credits: str
    _handlers: Dict[str, List[HandleFunction]]

    _queues: List[AbstractQueue]
    _response_exchange: AbstractExchange
    _connection: AbstractConnection
    _channel: AbstractChannel

    def __init__(self, service_name: str, connection_credits: str):
        self._service_name = service_name
        self._connection_credits = connection_credits
        self._handlers = defaultdict(list)
        self._queues = list()

    def bind(self, endpoint: str, handle_func: HandleFunction):
        self._handlers[endpoint].append(handle_func)
        print(f"Service: handle function {handle_func.__name__} bound to endpoint '{endpoint}'")

    def _get_endpoint_queue_name(self, endpoint: str) -> str:
        return "{}.{}".format(self._service_name, endpoint)

    async def _declare_endpoint_queues(self):
        for endpoint, handlers in self._handlers.items():
            queue_name = self._get_endpoint_queue_name(endpoint)
            endpoint_queue = await self._channel.declare_queue(queue_name)
            print(f"Service: Created endpoint queue '{endpoint_queue.name}'")

            for handle_func in handlers:
                handler = RequestHandler(handle_func, self._response_exchange)
                await endpoint_queue.consume(handler.handle_request)

    async def run(self):
        print("Service: Open connection...")
        self._connection = await aio_pika.connect(self._connection_credits)
        print("Service: Open channel...")
        self._channel = await self._connection.channel()
        print("Service: getting exchange...")
        self._response_exchange = self._channel.default_exchange
        print("Service: endpoint queues...")
        await self._declare_endpoint_queues()

    async def stop(self):
        print("Service: close channel...")
        await self._channel.close()
        print("Service: close connection...")
        await self._connection.close()

        for queue in self._queues:
            print("Service: closing queue...")
            await queue.close_callbacks()

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.stop())
