from typing import Optional
from decimal import Decimal
from datetime import date, datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

from app.models.schemas import OrderStatus


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str
    hashed_password: str
    is_admin: bool = False


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    cpf: str

    orders: list["Order"] = Relationship(
        back_populates="client", cascade_delete=True)


class Product(SQLModel, table=True):
    __tablename__ = "products"

    barcode: str = Field(primary_key=True, index=True)
    name: str
    description: str
    price: Decimal = Field(default=0, max_digits=19, decimal_places=4)
    category: str
    available: bool = False
    stock: int = 0
    section: str
    expiration_date: Optional[date] = None
    image_url: Optional[str] = None


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default=datetime.now(timezone.utc))
    client_id: int = Field(foreign_key="clients.id")

    items: list["OrderItem"] = Relationship(
        back_populates="order", cascade_delete=True)
    client: "Client" = Relationship(back_populates="orders")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: str = Field(foreign_key="products.barcode")
    quantity: int

    order: "Order" = Relationship(back_populates="items")
