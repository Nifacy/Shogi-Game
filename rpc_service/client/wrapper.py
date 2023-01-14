from typing import Any, Awaitable, Callable
from ..contract import ServiceEndpoint


CallMethod = Callable[[str, Any], Awaitable[Any]]


class CallWrapper:
    _endpoint: ServiceEndpoint
    _call_method: CallMethod

    def __init__(self, endpoint: ServiceEndpoint, call_method: CallMethod):
        self._endpoint = endpoint
        self._call_method = call_method

    async def __call__(self, **kwargs) -> Awaitable[Any]:
        deserialized = self._endpoint.request_message(**kwargs)
        return await self._call_method(self._endpoint.endpoint_name, deserialized)
