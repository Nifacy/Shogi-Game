from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import auth

app = FastAPI()

app.include_router(auth.router)


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)