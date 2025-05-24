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
