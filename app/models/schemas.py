from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel


class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class CreateUser(SQLModel):
    name: str
    cpf: str
    email: EmailStr
    password: str
