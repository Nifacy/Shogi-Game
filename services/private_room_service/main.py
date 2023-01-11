import asyncio
from random import randint
from typing import List, Dict
from pydantic import BaseModel

from amqp_events import AmqpEventPublisher
from rpc_service.handler import ResponseError
from rpc_service.service import RPCService
from services.private_room_service.adapters import SessionServiceAdapter


class Player(BaseModel):
    name: str


class PrivateRoom(BaseModel):
    players: List[Player]
    connection_key: str


class PrivateRoomInfo(BaseModel):
    connection_key: str


class SuccessMessage(BaseModel):
    message_type: str = "success"
    detail: str = "Success"


db: Dict[str, PrivateRoom] = dict()
service = RPCService("private_room_service", "amqp://guest:guest@localhost")
room_events_publisher = AmqpEventPublisher("private_room_service.rooms.events")
session_service_adapter = None


def generate_connection_key() -> str:
    while True:
        code = "".join(map(chr, [randint(65, 91) for _ in range(10)]))
        if code not in db:
            return code


async def add_player(connection_key: str, player_name: str):
    room = db[connection_key]
    room.players.append(Player(name=player_name))

    if len(room.players) >= 2:
        first_player = room.players[0].name
        second_player = room.players[1].name
        session = await session_service_adapter.create_session(first_player, second_player)

        await room_events_publisher.notify({
            "event_type": "SESSION_CREATED",
            "connection_key": connection_key,
            "session_id": session.session_id
        })

        del db[connection_key]


# Endpoint

async def create_private_room(player_name: str) -> PrivateRoomInfo:
    creator = Player(name=player_name)
    connection_key = generate_connection_key()
    room = PrivateRoom(players=[creator], connection_key=connection_key)
    db[connection_key] = room
    return PrivateRoomInfo(connection_key=connection_key)


async def connect_to_private_room(player_name: str, connection_key: str) -> SuccessMessage:
    if connection_key not in db:
        raise ResponseError(error_type="not_found", detail=f"Room with connection key {connection_key} not found")

    await add_player(connection_key, player_name)
    return SuccessMessage()


# Bindings


service.bind("create", create_private_room)
service.bind("connect", connect_to_private_room)


# Launch


async def main():
    global session_service_adapter

    session_service_adapter = SessionServiceAdapter()

    await room_events_publisher.connect()
    await session_service_adapter.connect()
    await service.run()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
