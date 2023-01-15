from fastapi import APIRouter, HTTPException
from fastapi.websockets import WebSocket

from amqp_events import AmqpEventListener
from contracts import session_service
from rpc_service import RpcClientBuilder
from services.gateway_service.dependencies import get_current_user
from services.gateway_service.websocket_formatters import ConnectionContext, WebSocketCommandReceiver, WebSocketSessionEventObserver


session_router = APIRouter()
session_service_client = RpcClientBuilder.from_contract(session_service.Contract)
session_events_listener = AmqpEventListener('session_service.sessions.events')


@session_router.on_event('startup')
async def open_connections():
    await session_service_client.connect('amqp://guest:guest@localhost')
    await session_events_listener.connect('amqp://guest:guest@localhost')


@session_router.on_event('shutdown')
async def close_connections():
    await session_service_client.close()
    await session_events_listener.close()


@session_router.websocket('/connect')
async def connect_to_game_session(websocket: WebSocket, token: str, session_id: int):
    await websocket.accept()

    try:
        user = await get_current_user(token)
    except HTTPException as e:
        await websocket.send_text(str(e))
        await websocket.close()
        return

    try:
        await session_service_client.connect_to_session(player_name=user.username, session_id=session_id)
    except (session_service.NotExists, session_service.AccessDenied) as e:
        await websocket.send_text(str(e))
        await websocket.close()
        return

    context = ConnectionContext(websocket=websocket, player_name=user.username, session_id=session_id)
    sender = WebSocketCommandReceiver(context, session_service_client)
    observer = WebSocketSessionEventObserver(context)

    session_events_listener.attach(observer)
    await sender.start_listen()
    session_events_listener.detach(observer)
    await websocket.close()
