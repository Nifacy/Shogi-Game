import dataclasses
import pydantic
from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Awaitable, Any, Iterable, Type
from .utils import build_request_message_type
from ..messages import RpcMessageGroup, SuccessMessage


_EndpointFunc = TypeVar('_EndpointFunc', bound=Callable[..., Awaitable[Any]])


@dataclasses.dataclass(frozen=True)
class ServiceEndpoint:
    """
    Объект - значение, хранящий информацию о точке входа сервиса

    Arguments:
        endpoint_name - название точки входа
        signature - сигнатура вызываемой функции со стороны сервиса
    """

    endpoint_name: str
    method_name: str
    request_message: Type[pydantic.BaseModel]


def endpoint(func: _EndpointFunc) -> _EndpointFunc:
    """
    Декоратор методов контракта. Помечает данный метод точкой входа сервиса.

    :param func: метод, через который происходит запрос к точке входа
    """

    func.__is_endpoint__ = True
    return abstractmethod(func)


class RpcContract(ABC):
    """
    Шаблон для интерфейсов - контрактов с сервисами.

    Arguments:
        __messages__ - объект группы сообщений, которые может отсылать сервис
        __service__ - название сервиса. По умолчанию будет равен названию класса контракта

    Usage:
    ``
    group = RpcMessagesGroup()

    @group.add_message_type
    class ExampleResponse(ResponseMessage):
        return_value: int

    class ExampleContract(RpcContract):
        __messages__ = group
        __service__ = 'example_service'

        @endpoint('endpoint_a')
        async def endpoint_a(x: int, y: int) -> ExampleResponse:
            raise NotImplementedError()
    ``
    """

    __messages__: RpcMessageGroup
    __service__: str

    @classmethod
    def _generate_endpoint_name(cls, endpoint: str) -> str:
        return f"{cls.service_name()}.{endpoint}"

    @classmethod
    def endpoints(cls) -> Iterable[ServiceEndpoint]:
        """
        Возвращает итерируемый объект, содержащий информацию о точках входа сервиса
        """

        endpoints = getattr(cls, "__endpoints__", [])

        if endpoints:
            return endpoints

        for attr in cls.__dict__.values():
            if getattr(attr, "__is_endpoint__", False):
                fullname = cls._generate_endpoint_name(attr.__name__)
                endpoints.append(ServiceEndpoint(
                    endpoint_name=fullname,
                    request_message=build_request_message_type(attr),
                    method_name=attr.__name__
                ))

        setattr(cls, "__endpoints__", endpoints)
        return tuple(endpoints)

    @classmethod
    def service_name(cls):
        """
        Возвращает название сервиса (если поле `__service__` не было указано, то возвращается имя интерфейса
        контракта)
        """

        return getattr(cls, "__service__", cls.__name__)

    @classmethod
    def messages(cls) -> RpcMessageGroup:
        """
        Возвращает группу всех связанных с контрактом сообщений (результаты, аргументы, исключения).
        """

        total = RpcMessageGroup()
        requests = RpcMessageGroup()
        responses = getattr(cls, "__messages__", RpcMessageGroup())

        for endpoint in cls.endpoints():
            requests.add_message_type(endpoint.request_message)

        total.add_message_type(requests)
        total.add_message_type(responses)
        total.add_message_type(SuccessMessage)

        return total
