from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from tortoise.exceptions import DoesNotExist

from app.dependencies import get_current_user
from app.models import User, PrivateRoom, Room
from app.schemas import PrivateRoomInfo, PrivateRoomConnectPost, AccountInfo


router = APIRouter()


@router.post("/connect", response_model=PrivateRoomInfo, status_code=status.HTTP_200_OK)
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


@router.post("/create", response_model=PrivateRoomInfo)
async def create_private_room(current_user: AccountInfo = Depends(get_current_user)):
    user = await User.get(id=current_user.id)

    if user.connected_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already connected to a room")

    room = await Room.create()
    private_room = await PrivateRoom.create(room=room, connection_key=str(room.id))

    user.connected_room = room
    await user.save()

    return PrivateRoomInfo(room_id=room.id, connect_key=private_room.connection_key)
