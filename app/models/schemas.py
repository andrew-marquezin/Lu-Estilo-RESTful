from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel


class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class CreateUser(SQLModel):
    email: EmailStr
    password: str


class CreateClient(SQLModel):
    name: str
    email: EmailStr
    cpf: str


class UpdateClient(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    cpf: str | None = None


class OrderItemCreate(SQLModel):
    product_id: str
    quantity: int


class OrderCreate(SQLModel):
    items: list[OrderItemCreate]
    client_id: int
