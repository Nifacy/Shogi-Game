from pydantic import BaseModel


class AccountInfo(BaseModel):
    username: str
    rating: int


class Registration(BaseModel):
    username: str
    password: str


class AccessData(BaseModel):
    access_token: str
    token_type: str


class PrivateRoom(BaseModel):
    room_id: int
    connect_key: str


class PrivateRoomConnectPost(BaseModel):
    connect_key: str


class FoundRoom(BaseModel):
    room_id: int
