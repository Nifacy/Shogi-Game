from typing import Optional

from app.models import User


async def authenticate_user(username: str, password: str) -> Optional[User]:
    user = await User.get(username=username)

    if not user:
        return None

    if not user.verify_password(password):
        return None

    return user
