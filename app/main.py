from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session, select
from app.db import create_db_and_tables, get_session
from app.auth.routes import router as auth_router
from app.models.tables import User


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app):
    print("executing pre-startup code")
    create_db_and_tables()
    yield
    # Cleanup code


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")


# @app.post("/users")
# async def create_user(user: dict,
#                       session: SessionDep):
#     db_user = User(**user)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user


@app.get("/clients")
async def read_user(session: SessionDep,
                    offset: int = 0,
                    limit: int = 10,):
    users = session.exec(select(User)).all()
    return users


@app.get("/clients/{id}")
async def read_one_user(id: int, session: SessionDep):
    ...


@app.put("/clients/{id}")
async def update_user(id: int, user: dict, session: SessionDep):
    ...


@app.delete("/clients/{id}")
async def delete_user(id: int, session: SessionDep):
    ...
