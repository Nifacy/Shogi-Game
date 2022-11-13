from pydantic import BaseModel


class Registration(BaseModel):
    username: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class AccountInfo(BaseModel):
    username: str
    rating: int


class AccessData(BaseModel):
    access_token: str
