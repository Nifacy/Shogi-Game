import asyncio

import jwt
from ddd_domain_events import DomainEvents
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import DecodeError
from starlette.websockets import WebSocket, WebSocketDisconnect
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError, DoesNotExist, NoValuesFetched

from app import settings
from app.actions import authenticate_user, send_command
from app.models import User, Room, PrivateRoom, Player
from app.room_message_sender import RoomMessageSender
from app.schemas import Registration, AccountInfo, AccessData, PrivateRoomConnectPost, PrivateRoomInfo, FoundRoom, RatingIncrement

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user = await User.get(id=payload.get('id'))

    except (DoesNotExist, DecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')

    return await AccountInfo.from_tortoise_orm(user)


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(registration_data: Registration):
    user_obj = User(username=registration_data.username,
                    password_hash=bcrypt.hash(registration_data.password))

    try:
        await user_obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username taken")


@app.post("/auth/login", response_model=AccessData, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect password or username")

    user_obj = await AccountInfo.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

    return AccessData(access_token=token, token_type='bearer')


@app.get("/users/me", response_model=AccountInfo, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: AccountInfo = Depends(get_current_user)):
    return current_user


@app.get("/users/info/{username}", response_model=AccountInfo, status_code=status.HTTP_302_FOUND)
async def get_user_info(username: str):
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")

    return await AccountInfo.from_tortoise_orm(user)


@app.post("/room/private/connect", response_model=PrivateRoomInfo, status_code=status.HTTP_200_OK)
async def connect_to_private_room(
        connect_data: PrivateRoomConnectPost = Depends(),
        current_user: AccountInfo = Depends(get_current_user)
):
    user = await User.get(id=current_user.id)

    if user.connected_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already connected to a room")

    try:
        private_room = await PrivateRoom.get(connection_key=connect_data.connect_key)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid connect key")

    room = await private_room.room.first()

    if room.state is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room closed")

    user.connected_room = room
    await user.save()

    return PrivateRoomInfo(room_id=room.id, connect_key=private_room.connection_key)


@app.post("/room/private/create", response_model=PrivateRoomInfo)
async def create_private_room(current_user: AccountInfo = Depends(get_current_user)):
    user = await User.get(id=current_user.id)

    if user.connected_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already connected to a room")

    room = await Room.create()
    private_room = await PrivateRoom.create(room=room, connection_key=str(room.id))

    user.connected_room = room
    await user.save()

    return PrivateRoomInfo(room_id=room.id, connect_key=private_room.connection_key)


@app.post("/room/search", response_model=FoundRoom)
async def find_opponent(
    increment: RatingIncrement = Depends(),
    current_user: AccountInfo = Depends(get_current_user)
):

    user = await User.get(id=current_user.id)

    if user.connected_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already connected to a room")

    if user.inWaiting:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already added to the waiting room")
    
    players_in_waiting = await Player.all()

    for player in players_in_waiting:
        y = await player.user
        if user.rating - increment.min < y.rating and y.rating < user.rating + increment.max:
            user.connected_room = await y.connected_room
            await user.save()
            await player.delete()
            break
    else:
        room = await Room.create()
        user.connected_room = room
        await user.save()
        player = await Player.create(user=user)

    room = await user.connected_room

    return FoundRoom(room_id=room.id)



@app.websocket("/room/connect")
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
