from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError
import jwt

from app.schemas import Registration, AccessData, AccountInfo
from app.models import User
from app.actions import authenticate_user
from app import settings

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(registration_data: Registration):
    user_obj = User(username=registration_data.username,
                    password_hash=bcrypt.hash(registration_data.password))

    try:
        await user_obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username taken")


@router.post("/login", response_model=AccessData, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect password or username")

    user_obj = await AccountInfo.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

    return AccessData(access_token=token, token_type='bearer')