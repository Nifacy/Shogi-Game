import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.actions import send_command

from app.models import Room, User


router = APIRouter()


@router.websocket("/room/connect")
async def connect_to_game_session(websocket: WebSocket, token: str, room_id: int):
    await websocket.accept()

    try:
        user = await get_current_user(token=token)
        user = await User.get(id=user.id)
    except HTTPException:
        await websocket.send_text("exception.security.unauthorized")
        await websocket.close()
        return

    if not await Room.exists(id=room_id):
        await websocket.send_text("exception.room.doesnt_exist")
        await websocket.close()
        return

    room = await user.connected_room.first() if user.connected_room else None

    if not room or room_id != room.id:
        await websocket.send_text("exception.security.access_denied")
        await websocket.close()
        return

    with DomainEvents() as domain_events:
        sender = RoomMessageSender(
            room_id=room_id,
            user_id=user.id,
            connection=websocket,
            events_context=domain_events,
            loop=asyncio.get_event_loop()
        )

        while True:
            try:
                command = await websocket.receive_json()
                print("RECEIVED COMMAND:", command)
                await send_command(room_id=room_id, command=command, user_id=user.id)
            except WebSocketDisconnect:
                break

        sender.stop()

    await websocket.close()


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
