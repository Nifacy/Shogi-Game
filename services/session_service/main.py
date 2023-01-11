import asyncio

from ddd_domain_events import DomainEventCallable
from pydantic import BaseModel

from app.state_converter import encode_state
from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import GameState
from rpc_service.handler import ResponseError
from services.session_service.domain.adapters import NotExists
from services.session_service.command_parser import parse_command
from services.session_service.domain.models import PlayerNotInSession, PlayerModel
from services.session_service.domain.usecases import *
from services.session_service.infrastructure.session_database import DefaultSessionDatabase

from amqp_events import AmqpEventPublisher
from rpc_service.service import RPCService


# Models


class SuccessMessage(BaseModel):
    message_type: str = "success"
    detail: str = "Success"


class Session(BaseModel):
    session_id: int
    first_player: str
    second_player: str


# Init infrastructure


service = RPCService(service_name="session_service", connection_credits="amqp://guest:guest@localhost")
room_event_publisher = AmqpEventPublisher(event_name="session_service.sessions.events")

db = DefaultSessionDatabase()


# Endpoints


async def create_session(first_player: str, second_player: str) -> Session:
    created_session = CreateSession(storage=db)(first_player_name=first_player, second_player_name=second_player)
    players = created_session.get_players()
    response = Session(
        session_id=created_session.id,
        first_player=players[0].name,
        second_player=players[1].name
    )

    return response


async def connect_to_session(session_id: int, player_name: str) -> SuccessMessage:
    try:
        ConnectToSession(storage=db)(session_id=session_id, player_name=player_name)
    except PlayerNotInSession as e:
        raise ResponseError(error_type="access_denied", detail=str(e))
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=str(e))

    return SuccessMessage()


async def disconnect_from_session(session_id: int, player_name: str) -> SuccessMessage:
    try:
        DisconnectFromSession(storage=db)(session_id=session_id, player_name=player_name)
    except PlayerNotInSession as e:
        raise ResponseError(error_type="access_denied", detail=str(e))
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=str(e))

    return SuccessMessage()


async def execute_command(session_id: int, player_name: str, command: dict) -> SuccessMessage:
    try:
        player = GetPlayer(db)(player_name, session_id)
        parsed_command = parse_command(player, command)
        ExecuteCommand(db)(session_id, parsed_command)
    except ExecuteCommandException as e:
        raise ResponseError(error_type=f"execute_error.{type(e).__name__}", detail=str(e))
    except PlayerNotInSession as e:
        raise ResponseError(error_type="access_denied", detail=str(e))
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=str(e))
    return SuccessMessage()


async def get_session_game_state(session_id: int) -> dict:
    try:
        session = await GetSession(db)(session_id=session_id)
    except NotExists as e:
        raise ResponseError(error_type="not_exists", detail=str(e))

    return encode_state(session.state)


# Event handlers

# TODO: Move on events lib: pip install events

async def on_state_changed(session_id: int, changed_state: GameState):
    message = {
        "event_type": SessionEvents.STATE_CHANGED.value,
        "session_id": session_id,
        "changed_state": encode_state(changed_state)
    }

    await room_event_publisher.notify(message)


async def on_player_connected(session_id: int, player_name: str):
    message = {
        "event_type": SessionEvents.PLAYER_CONNECTED.value,
        "session_id": session_id,
        "player_name": player_name
    }

    await room_event_publisher.notify(message)


async def on_player_disconnected(session_id: int, player_name: str):
    message = {
        "event_type": SessionEvents.PLAYER_DISCONNECTED.value,
        "session_id": session_id,
        "player_name": player_name
    }

    await room_event_publisher.notify(message)


async def on_game_ended(session_id: int, winner: PlayerModel):
    message = {
        "event_type": SessionEvents.GAME_ENDED.value,
        "session_id": session_id,
        "winner": winner.name
    }

    await room_event_publisher.notify(message)


# Bindings


service.bind("create", create_session)
service.bind("connect", connect_to_session)
service.bind("disconnect", disconnect_from_session)
service.bind("execute", execute_command)
service.bind("get_state", get_session_game_state)


event_callbacks = {
    SessionEvents.STATE_CHANGED: on_state_changed,
    SessionEvents.PLAYER_CONNECTED: on_player_connected,
    SessionEvents.PLAYER_DISCONNECTED: on_player_disconnected,
    SessionEvents.GAME_ENDED: on_game_ended
}


def async_event_callable_wrapper(callback):
    def sync_callback(*args, **kwargs):
        print(f"Called {callback.__name__}")
        asyncio.create_task(callback(*args, **kwargs))

    return sync_callback


async def main():
    await service.run()
    await room_event_publisher.connect()

    with DomainEvents() as context:
        for event, callback in event_callbacks.items():
            event_callable = DomainEventCallable(event, callback=async_event_callable_wrapper(callback))
            context.register_event(event_callable)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
