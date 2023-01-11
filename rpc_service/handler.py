import inspect
import json
import logging
from typing import Callable, Any, Awaitable, Type

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, AbstractExchange
from pydantic import ValidationError, BaseModel, create_model


HandleFunction = Callable[..., Awaitable[BaseModel]]


def build_arguments_model(func: HandleFunction) -> Type[BaseModel]:
    fields = dict()

    for name, info in inspect.signature(func).parameters.items():
        annotation = info.annotation if info.annotation != inspect.Signature.empty else Any
        default = info.default if info.default != inspect.Signature.empty else ...

        fields[name] = (annotation, default)

    print(f"building: {fields}")
    return create_model(f"{func.__name__}_arguments", **fields)


class ResponseError(Exception):
    def __init__(self, error_type: str, detail: str):
        self.error_type = error_type
        self.detail = detail

    def json(self) -> str:
        error_info = {
            "error_type": f"error.{self.error_type}",
            "detail": self.detail
        }

        return json.dumps(error_info)


class InternalError(ResponseError):
    def __init__(self):
        super().__init__(error_type="internal", detail="Internal error")


class RequestHandler:
    _handle_function: HandleFunction
    _exchange: AbstractExchange
    _arguments_model: Type[BaseModel]

    def __init__(self, handle_function: HandleFunction, exchange: AbstractExchange):
        self._handle_function = handle_function
        self._exchange = exchange
        self._arguments_model = build_arguments_model(handle_function)
        print(self._arguments_model)

    def _validate_request_body(self, request: AbstractIncomingMessage) -> BaseModel:
        print("validate: parse to json...")
        data = json.loads(request.body.decode())
        print(f"validate: parsed {data}")

        print("validate: validate with arguments model")
        decoded_data = self._arguments_model(**data)
        print(f"validate: validated {decoded_data}")
        return decoded_data

    async def handle_request(self, request: AbstractIncomingMessage):
        async with request.process():
            if request.reply_to is None:
                print("Without reply queue")
                return

            print("get request")

            try:
                decoded_request = self._validate_request_body(request)
                decoded_request = {field: getattr(decoded_request, field) for field in decoded_request.__fields__.keys()}
                response = await self._handle_function(**decoded_request)
                response = response.json()
            except (ValidationError, ResponseError) as e:
                response = e.json()
            except Exception as e:
                logging.exception(str(e))
                response = InternalError().json()

            print(f"send response: {response} to {request.reply_to}")

            response_message = Message(
                body=response.encode(),
                correlation_id=request.correlation_id
            )

            await self._exchange.publish(response_message, routing_key=request.reply_to)
