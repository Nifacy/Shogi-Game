from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import auth, opponent_search, private_room, room_connection, users

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(opponent_search.router, prefix="/opponent")
app.include_router(private_room.router, prefix="/private-room")
app.include_router(room_connection.router, prefix="/room-session")
app.include_router(users.router, prefix="/users")


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)