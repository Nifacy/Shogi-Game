from typing import TypeVar, Type

from .base import BaseRpcClient
from .wrapper import CallWrapper
from ..contract import RpcContract


_Contract = TypeVar('_Contract', bound=Type[RpcContract])


class RpcClientBuilder:
    @staticmethod
    def from_contract(contract: _Contract) -> BaseRpcClient | _Contract:
        client = BaseRpcClient(contract.messages())

        for endpoint in contract.endpoints():
            setattr(client, endpoint.method_name, CallWrapper(endpoint, client.call))

        return client
