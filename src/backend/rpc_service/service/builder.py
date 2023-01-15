from typing import TypeVar, Type

from .base import BaseRpcService
from ..contract import RpcContract


_Contract = TypeVar('_Contract', bound=RpcContract)


class RpcServiceBuilder:
    """
    Реализация паттерна 'Строитель'. Генерирует объект сервиса на основе реализации `implementation`, удовлетворяющей
    контракту `contract`
    """

    @staticmethod
    def from_contract(implementation: _Contract, contract: Type[_Contract]) -> BaseRpcService:
        service = BaseRpcService(messages=contract.messages())

        for endpoint in contract.endpoints():
            service.add_implementation(endpoint=endpoint, method=getattr(implementation, endpoint.method_name))

        return service
