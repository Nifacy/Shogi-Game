from dataclasses import dataclass
from rpc_service import RpcMessageGroup, ResponseMessage, ErrorResponse, RpcContract, endpoint


messages = RpcMessageGroup()


@messages.add_message_type
class PrivateRoomInfo(ResponseMessage):
    connection_key: str


@messages.add_message_type
@dataclass
class RoomNotFound(ErrorResponse):
    connection_key: str
    _message: str = 'Room with connection key {connection_key!r} not found'


@messages.add_message_type
@dataclass
class PlayerNotConnected(ErrorResponse):
    connection_key: str
    player_name: str
    _message: str = 'Player {player_name!r} not connected to room {connection_key!r}'


class Contract(RpcContract):
    __service__ = 'private_rooms'
    __messages__ = messages

    @endpoint
    async def create(self, player_name: str) -> PrivateRoomInfo:
        raise NotImplementedError()

    @endpoint
    async def connect_room(self, player_name: str, connection_key: str):
        raise NotImplementedError()

    @endpoint
    async def disconnect_room(self, player_name: str, connection_key: str):
        raise NotImplementedError()
