from dataclasses import dataclass
import pydantic
from rpc_service import RpcMessageGroup, ErrorResponse, RpcContract, endpoint


messages = RpcMessageGroup()


class SearchParameters(pydantic.BaseModel):
    min_rating: int
    max_rating: int


class CallerInfo(pydantic.BaseModel):
    name: str
    rating: int


@messages.add_message_type
@dataclass
class SearchAlreadyStarted(ErrorResponse):
    caller: CallerInfo
    _message: str = 'Search already started. Please, cancel last search'


@messages.add_message_type
@dataclass
class SearchNotStarted(ErrorResponse):
    caller: CallerInfo
    _message: str = 'Search not started'


class Contract(RpcContract):
    __service__ = 'searcher_service'
    __messages__ = messages

    @endpoint
    async def start_search(self, caller: CallerInfo, parameters: SearchParameters):
        raise NotImplementedError()

    @endpoint
    async def cancel_search(self, caller: CallerInfo):
        raise NotImplementedError()
