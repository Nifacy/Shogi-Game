import uvicorn
from fastapi import FastAPI
from services.gateway_service import routers


app = FastAPI()

app.include_router(routers.users_router, prefix='/users')
app.include_router(routers.auth_router, prefix='/auth')
app.include_router(routers.private_room_router, prefix='/room')
app.include_router(routers.session_router, prefix='/session')
app.include_router(routers.searcher_router, prefix='/search')

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
