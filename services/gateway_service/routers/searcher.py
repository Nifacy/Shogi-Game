from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.websockets import WebSocket

from amqp_events import AmqpEventListener
from amqp_events.utils import wait_for_publish
from contracts import searcher_service
from rpc_service import RpcClientBuilder
from services.gateway_service import schemas
from services.gateway_service.dependencies import get_current_user

searcher_router = APIRouter()
searcher_listener = AmqpEventListener('searcher_service.events')
searcher_service_client = RpcClientBuilder.from_contract(searcher_service.Contract)


@searcher_router.on_event('shutdown')
async def close_connections():
    await searcher_listener.close()
    await searcher_service_client.close()


@searcher_router.on_event('startup')
async def open_connections():
    await searcher_listener.connect('amqp://guest:guest@localhost')
    await searcher_service_client.connect('amqp://guest:guest@localhost')


@searcher_router.post('/start')
async def start_search(
        parameters: schemas.SearchParameters,
        current_user: schemas.AccountInfo = Depends(get_current_user)):
    caller = searcher_service.CallerInfo(name=current_user.username, rating=current_user.rating)
    params = searcher_service.SearchParameters(**parameters.dict())

    try:
        await searcher_service_client.start_search(parameters=params, caller=caller)
    except searcher_service.SearchAlreadyStarted as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return 'Success'


@searcher_router.post('/cancel')
async def end_search(current_user: schemas.AccountInfo = Depends(get_current_user)):
    caller = searcher_service.CallerInfo(name=current_user.username, rating=current_user.rating)

    try:
        await searcher_service_client.cancel_search(caller=caller)
    except searcher_service.SearchNotStarted as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return 'Success'


@searcher_router.websocket('/wait')
async def wait_for_opponent_connect(token: str, websocket: WebSocket):
    await websocket.accept()

    try:
        user = await get_current_user(token)
    except HTTPException as e:
        await websocket.send_text(e.detail)
        await websocket.close()
        return

    event_message = await wait_for_publish(
        lambda msg: (msg.get('event_type'), msg.get('caller')) == ('FOUND_OPPONENT', user.username),
        searcher_listener
    )

    await websocket.send_json({
        'event_type': event_message['event_type'],
        'session_id': event_message['session_id']
    })

    await websocket.close()
