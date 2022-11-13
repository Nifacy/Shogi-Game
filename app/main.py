from fastapi import FastAPI, Depends
from starlette.websockets import WebSocket

from app.dependecies.auth import get_active_user
from app.schemas.account import Registration, Login, AccountInfo, AccessData
from app.schemas.opponent_search import FoundRoomInfo
from app.schemas.private_room import PrivateRoomConnect, PrivateRoomInfo

app = FastAPI()


@app.post("/auth/register")
async def register(registration_data: Registration):
    raise NotImplementedError


@app.post("/auth/login")
async def login(form_data: Login) -> AccessData:
    raise NotImplementedError


@app.get("/users/me")
async def read_users_me(current_user: AccountInfo = Depends(get_active_user)) -> AccountInfo:
    raise NotImplementedError


@app.get("/users/info/{username}")
async def get_user_info(username: str) -> AccountInfo:
    raise NotImplementedError


@app.post("/session/private/connect")
async def connect_ro_private_session(
        connect_data: PrivateRoomConnect,
        current_user: AccountInfo = Depends(get_active_user)
) -> PrivateRoomInfo:
    raise NotImplementedError


@app.post("/session/private/create")
async def create_private_session(current_user: AccountInfo = Depends(get_active_user)) -> PrivateRoomInfo:
    raise NotImplementedError


@app.post("/session/search")
async def find_opponent(user: AccountInfo = Depends(get_active_user)) -> FoundRoomInfo:
    raise NotImplementedError


@app.websocket("/session/connect")
async def connect_to_game_session(websocket: WebSocket, session_id: int, access_data: AccessData):
    raise NotImplementedError
