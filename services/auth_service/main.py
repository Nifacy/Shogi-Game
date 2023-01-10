import asyncio
from typing import Union

import jwt
from jwt import DecodeError
from passlib.context import CryptContext
from pydantic import BaseModel


# Config
from rpc_service.handler import ResponseError
from rpc_service.service import RPCService

SECRET_KEY = "MY_WIFE_LEFT_ME"
ALGORITHM = "HS256"


# Schemas


class Registration(BaseModel):
    username: str
    password: str


class AuthData(BaseModel):
    username: str
    password: str


class UserCredits(BaseModel):
    username: str
    hashed_password: str


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Support functions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def generate_token(data: TokenData) -> str:
    return jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(database: dict, username: str, password: str) -> Union[UserCredits, None]:
    if username not in database:
        return None

    raw_data = database[username]
    user_credits = UserCredits(username=raw_data["username"], hashed_password=raw_data["hashed_password"])
    verify_result = verify_password(password, user_credits.hashed_password)

    if not verify_result:
        return None

    return user_credits


def decode_token(token: str) -> TokenData:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    token_data = TokenData(username=payload["username"])
    return token_data


# App

service = RPCService("auth_service", "amqp://guest:guest@localhost")
db = dict()


async def register(registration_data: Registration) -> Token:
    user_credits = UserCredits(
        username=registration_data.username,
        hashed_password=hash_password(registration_data.password))

    if user_credits.username in db:
        raise ResponseError(error_type="taken", detail="Username taken")

    db[user_credits.username] = user_credits.dict()
    token_data = TokenData(username=user_credits.username)
    token = Token(access_token=generate_token(token_data), token_type="bearer")

    return token


async def auth_user(auth_data: AuthData):
    user_credits = authenticate_user(db, auth_data.username, auth_data.password)

    if not user_credits:
        raise ResponseError(error_type="invalid_credits", detail="Incorrect password or username")

    token_data = TokenData(username=user_credits.username)
    token = Token(access_token=generate_token(token_data), token_type="bearer")

    return token


async def verify_user(token: str) -> TokenData:
    try:
        token_data = decode_token(token)
    except DecodeError:
        raise ResponseError(error_type="invalid_credits", detail='Invalid credentials')

    if token_data.username not in db:
        raise ResponseError(error_type="invalid_credits", detail='Invalid credentials')

    return token_data

# Bindings

service.bind("register", register)
service.bind("generate_token", auth_user)
service.bind("decode_token", verify_user)


async def main():
    await service.run()
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
