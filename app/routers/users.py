from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.exceptions import DoesNotExist

from app.dependencies import get_current_user
from app.models import User
from app.schemas import AccountInfo

router = APIRouter()


@router.get("/create", response_model=AccountInfo, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: AccountInfo = Depends(get_current_user)):
    return current_user


@router.get("/info/{username}", response_model=AccountInfo, status_code=status.HTTP_302_FOUND)
async def get_user_info(username: str):
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")

    return await AccountInfo.from_tortoise_orm(user)
