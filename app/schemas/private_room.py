from pydantic import BaseModel


class PrivateRoomConnect(BaseModel):
    connection_key: str


class PrivateRoomInfo(BaseModel):
    room_id: int
    connection_key: str
