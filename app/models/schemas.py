from enum import Enum
from decimal import Decimal
from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CreateClient(BaseModel):
    name: str
    email: EmailStr
    cpf: str = Field(max_length=11, pattern=r"^\d{11}$")


class UpdateClient(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    cpf: str | None = None


class OrderRead(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime


class ClientWithOrders(BaseModel):
    id: int
    name: str
    email: EmailStr
    cpf: str
    orders: list[OrderRead] = []


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    client_id: int


class OrderResponse(BaseModel):
    detail: str
    order_id: int


class ProductCreate(BaseModel):
    barcode: str = Field(min_length=13, max_length=13, pattern=r"^\d{13}$")
    name: str
    description: str
    price: Decimal
    category: str
    available: Optional[bool] = True
    stock: Optional[int] = 0
    section: str
    expiration_date: Optional[date] = None


class OrderReadWithItems(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    client_id: int
    items: list[OrderItemCreate] = []


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    client_id: Optional[int] = None
    items: Optional[list[OrderItemCreate]] = None


class ProductRead(BaseModel):
    barcode: str
    name: str
    description: str
    price: Decimal
    category: str
    available: bool
    stock: int
    section: str
    expiration_date: Optional[date] = None
