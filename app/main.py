from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db import create_db_and_tables, get_session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app):
    print("executing pre-startup code")
    create_db_and_tables()
    yield
    # Cleanup code

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
