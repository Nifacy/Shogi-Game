from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.websockets import WebSocket
from app.schemas import Registration, AccountInfo, AccessData, PrivateRoomConnectPost, PrivateRoom, FoundRoom

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependencies


async def get_current_user(token: str = Depends(oauth2_scheme)):
    raise NotImplementedError


# Endpoints


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(registration_data: Registration):
    raise NotImplementedError


@app.post("/auth/login", response_model=AccessData, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    raise NotImplementedError


@app.get("/users/me", response_model=AccountInfo, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: AccountInfo = Depends(get_current_user)):
    raise NotImplementedError


@app.get("/users/info/{username}")
async def get_user_info(username: str) -> AccountInfo:
    raise NotImplementedError


@app.post("/room/private/connect", response_model=PrivateRoom)
async def connect_ro_private_session(
        connect_data: PrivateRoomConnectPost = Depends(),
        current_user: AccountInfo = Depends(get_current_user)
):
    raise NotImplementedError


@app.post("/room/private/create", response_model=PrivateRoom)
async def create_private_room(current_user: AccountInfo = Depends(get_current_user)):
    raise NotImplementedError


@app.post("/room/search", response_model=FoundRoom)
async def find_opponent(user: AccountInfo = Depends(get_current_user)):
    raise NotImplementedError


@app.websocket("/room/connect")
async def connect_to_game_session(websocket: WebSocket, session_id: int, access_data: AccessData):
    raise NotImplementedError
