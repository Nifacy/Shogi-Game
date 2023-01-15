from fastapi import APIRouter, Depends, HTTPException
from fastapi.websockets import WebSocket
from starlette import status

from amqp_events import AmqpEventListener
from amqp_events.utils import wait_for_publish
from contracts import private_room_service
from rpc_service import RpcClientBuilder
from services.gateway_service import schemas
from services.gateway_service.dependencies import get_current_user

from services.gateway_service.settings import settings


private_room_router = APIRouter()
private_room_listener = AmqpEventListener('private_room_service.events')
private_room_service_client = RpcClientBuilder.from_contract(private_room_service.Contract)


@private_room_router.on_event('startup')
async def open_connections():
    await private_room_listener.connect(settings.amqp_dsn)
    await private_room_service_client.connect(settings.amqp_dsn)


@private_room_router.on_event('shutdown')
async def close_connections():
    await private_room_listener.close()
    await private_room_service_client.close()


@private_room_router.post('/create')
async def create_private_room(current_user: schemas.AccountInfo = Depends(get_current_user)) -> schemas.PrivateRoomInfo:
    room = await private_room_service_client.create(player_name=current_user.username)
    return schemas.PrivateRoomInfo(connection_key=room.connection_key)


@private_room_router.post('/connect')
async def connect_to_private_room(
        connection_key: str,
        current_user: schemas.AccountInfo = Depends(get_current_user)):
    try:
        await private_room_service_client.connect_room(
            player_name=current_user.username,
            connection_key=connection_key)

    except private_room_service.RoomNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return 'Success'


@private_room_router.post('/close')
async def close_private_room(
        connection_key: str,
        current_user: schemas.AccountInfo = Depends(get_current_user)):
    try:
        await private_room_service_client.disconnect_room(
            player_name=current_user.username,
            connection_key=connection_key)

    except private_room_service.RoomNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except private_room_service.PlayerNotConnected as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return 'Success'


@private_room_router.websocket('/wait')
async def wait_for_opponent_connect(token: str, connection_key: str, websocket: WebSocket):
    await websocket.accept()

    try:
        await get_current_user(token)
    except HTTPException as e:
        await websocket.send_text(e.detail)
        await websocket.close()
        return

    event_message = await wait_for_publish(
        lambda msg: (msg.get('event_type'), msg.get('connection_key')) == ('OPPONENT_CONNECTED', connection_key),
        private_room_listener
    )

    await websocket.send_json({
        'event_type': event_message['event_type'],
        'session_id': event_message['session_id']
    })
    await websocket.close()
