from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel
from db import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield
    # Cleanup code


@app.get("/")
def read_root():
    return {"Hello": "World"}
