import asyncio
import json
import uuid
from asyncio import Future
from typing import Dict

from aio_pika import connect, Message
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractIncomingMessage


class BaseRpcClient:
    _service_name: str
    _connection_credentials: str

    _futures: Dict[str, asyncio.Future]
    _loop: asyncio.AbstractEventLoop

    _connection: AbstractConnection
    _channel: AbstractChannel
    _callback_queue: AbstractQueue

    def __init__(self, service_name: str, credentials: str):
        self._service_name = service_name
        self._connection_credentials = credentials
        self._futures = dict()
        self._loop = asyncio.get_running_loop()

    async def connect(self):
        self._connection = await connect(self._connection_credentials, loop=self._loop)
        self._channel = await self._connection.channel()
        self._callback_queue = await self._channel.declare_queue(exclusive=True)

        await self._callback_queue.consume(self._on_response)

    async def _send_request(self, endpoint: str, request: dict) -> Future:
        correlation_id = str(uuid.uuid4())
        future = self._loop.create_future()
        endpoint_queue = "{}.{}".format(self._service_name, endpoint)

        self._futures[correlation_id] = future

        request_message = Message(
            json.dumps(request).encode(),
            content_type="application/json",
            correlation_id=correlation_id,
            reply_to=self._callback_queue.name
        )

        await self._channel.default_exchange.publish(request_message, routing_key=endpoint_queue)
        return future

    async def _on_response(self, message: AbstractIncomingMessage):
        if message.correlation_id is None:
            print(f"RpcClient: Bad message {message!r}")
            return

        future = self._futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def _call(self, endpoint: str, request: dict) -> dict:
        future = await self._send_request(endpoint, request)
        result = await future
        decoded_result = json.loads(result.decode())

        return decoded_result
