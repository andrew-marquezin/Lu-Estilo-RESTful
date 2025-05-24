from typing import Optional
from decimal import Decimal
from datetime import date

from sqlmodel import SQLModel, Field, Relationship

from app.models.schemas import OrderStatus


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str
    hashed_password: str


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    cpf: str

    orders: list["Order"] = Relationship(back_populates="client")


class Product(SQLModel, table=True):
    __tablename__ = "products"

    barcode: str = Field(primary_key=True, index=True)
    description: str
    price: Decimal = Field(default=0, max_digits=19, decimal_places=4)
    category: str
    available: bool = Field(default=True)
    stock: int = Field(default=0)
    session: str
    expiration_date: date = Field(default=None)


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING.value)
    client_id: int = Field(foreign_key="clients.id")

    client: "Client" = Relationship(back_populates="orders")
