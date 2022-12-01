from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist
import jwt
from jwt import DecodeError

from app import settings
from app.models import User
from app.schemas import AccountInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user = await User.get(id=payload.get('id'))

    except (DoesNotExist, DecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')

    return await AccountInfo.from_tortoise_orm(user)