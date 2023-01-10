import asyncio
from typing import Dict, Union
from pydantic import BaseModel

from amqp_events import AmqpEventPublisher
from rpc_service.handler import ResponseError
from rpc_service.service import RPCService
from services.private_room_service.adapters import SessionServiceAdapter


class SearchParameters(BaseModel):
    min_rating: int
    max_rating: int


class WaitingPlayer(BaseModel):
    name: str
    rating: int
    parameters: SearchParameters


class SuccessMessage(BaseModel):
    message_type: str = "success"
    detail: str = "Success"


db: Dict[str, WaitingPlayer] = dict()
service = RPCService("searcher_service", "amqp://guest:guets@localhost")
room_events_publisher = AmqpEventPublisher("searcher_service.search.events")
session_service_adapter = SessionServiceAdapter()


def find_player(parameters: SearchParameters) -> Union[None, WaitingPlayer]:
    for waiting_player in db.values():
        if parameters.min_rating <= waiting_player.rating <= parameters.max_rating:
            return waiting_player


async def notify_about_opponent_found(created_session_id: int, waiting_player_name: str):
    await room_events_publisher.notify({
        "event_type": "FOUND",
        "target": waiting_player_name,
        "created_session": created_session_id
    })


async def create_session(first_player: str, second_player: str):
    session = await session_service_adapter.create_session(first_player, second_player)
    await notify_about_opponent_found(session.session_id, first_player)
    await notify_about_opponent_found(session.session_id, second_player)


# Endpoint


async def start_search(player_name: str, rating: int, parameters: SearchParameters) -> SuccessMessage:
    if player_name in db:
        raise ResponseError(error_type="already_started", detail=f"Search opponent for player {player_name!r} already started")

    opponent = find_player(parameters)

    if opponent is not None:
        await create_session(player_name, opponent.name)
    else:
        db[player_name] = WaitingPlayer(name=player_name, rating=rating, parameters=parameters)

    return SuccessMessage()


async def cancel_search(player_name: str) -> SuccessMessage:
    if player_name not in db:
        raise ResponseError(error_type="not_found", detail=f"Search for player {player_name!r} not started")

    del db[player_name]
    return SuccessMessage()


# Bindings


service.bind("start", start_search)
service.bind("cancel", cancel_search)


async def main():
    await room_events_publisher.connect()
    await service.run()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
