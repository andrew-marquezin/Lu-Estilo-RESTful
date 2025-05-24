from contextlib import asynccontextmanager

from fastapi import FastAPI
from .db import create_db_and_tables
from .auth.routes import router as auth_router
from .routes import clients


@asynccontextmanager
async def lifespan(app):
    print("executing pre-startup code")
    create_db_and_tables()
    yield
    # Cleanup code


app = FastAPI(lifespan=lifespan)

app.include_router(clients.router, prefix="/clients")
app.include_router(auth_router, prefix="/auth")
