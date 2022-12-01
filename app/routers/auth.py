from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError

from ..schemas import Registration, AccessData, AccountInfo
from ..models import User
from ..actions import authenticate_user

router = APIRouter()

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(registration_data: Registration):
    user_obj = User(username=registration_data.username,
                    password_hash=bcrypt.hash(registration_data.password))

    try:
        await user_obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username taken")


@router.post("/auth/login", response_model=AccessData, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect password or username")

    user_obj = await AccountInfo.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

    return AccessData(access_token=token, token_type='bearer')