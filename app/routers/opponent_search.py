from fastapi import APIRouter, status, Depends, HTTPException

from app.models import User, Room, Player
from app.schemas import FoundRoom, RatingIncrement, AccountInfo
from app.dependencies import get_current_user
router = APIRouter()

@router.post("/search", response_model=FoundRoom)
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