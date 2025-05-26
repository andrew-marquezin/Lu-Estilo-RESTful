from datetime import timedelta

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.dependencies import (
    authenticate_user,
    get_user_from_token
)
from app.auth.schemas import Token, TokenPair
from app.auth.utils import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.db import get_session
from app.models.schemas import CreateUser
from app.models.tables import User

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["auth"])


@router.post("/register")
async def register_user(
    user: CreateUser,
    session: SessionDep
):
    existing_user = session.exec(
        select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token", response_model=TokenPair)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    current_user: Annotated[User, Depends(
        get_user_from_token("refresh_token"))]
):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_user_from_token("access_token"))]
):
    return current_user
