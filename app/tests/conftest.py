import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import event


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={
                       "check_same_thread": False})


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    SQLModel.metadata.create_all(engine)
    yield
    # Opcional: apagar arquivo após testes
    # import os
    # os.remove("./test.db")


@pytest.fixture(scope="session")
def session():
    with Session(engine) as session:
        yield session
