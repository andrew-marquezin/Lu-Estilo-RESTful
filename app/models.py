from typing import Optional
from decimal import Decimal
from datetime import date
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    cpf: str

    orders: list["Order"] = Relationship(back_populates="client")


class Product(SQLModel, table=True):
    barcode: str = Field(primary_key=True, index=True)
    description: str
    price: Decimal = Field(default=0, max_digits=19, decimal_places=4)
    category: str
    available: bool = Field(default=True)
    stock: int = Field(default=0)
    session: str
    expiration_date: date = Field(default=None)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING.value)
    client_id: int = Field(foreign_key="client.id")

    client: "Client" = Relationship(back_populates="orders")
