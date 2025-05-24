from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.auth.schemas import TokenData
from app.auth.utils import ALGORITHM, SECRET_KEY, verify_password
from app.db import get_session
from app.models.tables import User


SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = session.exec(
        select(User).where(User.email == token_data.username)
    ).first()
    if user is None:
        raise credentials_exception
    return user


def get_user(db: SessionDep, email: str):
    if email is None:
        return None
    user = db.exec(
        select(User).where(User.email == email)
    ).first()
    return user


def authenticate_user(email: str, password: str, db):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
