from pydantic import BaseModel


class FoundRoomInfo(BaseModel):
    room_id: int
