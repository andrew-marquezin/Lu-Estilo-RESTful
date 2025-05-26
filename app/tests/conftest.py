import os

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import event

from app.models.tables import Client, Product


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
    os.remove("./test.db")


@pytest.fixture(scope="session")
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def test_client_obj(session):
    client = Client(
        name="Other Test Client",
        email="test@example.com",
        cpf="01987654321"
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@pytest.fixture(scope="session", autouse=True)
def test_product_obj(session):
    product = Product(
        barcode="3210987654321",
        name="Other Test Product",
        description="A second product for testing",
        category="Test Category",
        price=19.99,
        stock=100,
        available=True,
        section="Test Section",
        expiration_date=None,
        image_url=None
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
