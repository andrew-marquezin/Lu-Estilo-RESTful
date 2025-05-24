import os

from sqlmodel import create_engine, Session
import app.models.tables as models

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
