from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User

AccountInfo = pydantic_model_creator(cls=User, name='AccountInfo')


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
