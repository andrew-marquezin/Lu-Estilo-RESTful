from typing import Annotated, Optional
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.utils import error_responses
from app.db import get_session
from app.models.tables import Order, Product, OrderItem, Client
from app.models.schemas import (OrderCreate,
                                OrderItemCreate,
                                OrderReadWithItems,
                                OrderStatus)


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["orders"])


def check_product_availability_and_stock(
        item: OrderItemCreate, session: SessionDep):
    if item.quantity <= 0:
        raise error_responses.EXCEPTION_400
    product = session.exec(
        select(Product).where(Product.barcode == item.product_id)
    ).first()
    if not product or not product.available:
        raise error_responses.product_not_found(item.product_id)
    if product.stock < item.quantity:
        raise error_responses.insufficient_stock(
            product.barcode, product.name
        )


@router.post("/", status_code=201)
async def create_order(
    order_data: OrderCreate,
    session: SessionDep
):
    client = session.exec(
        select(Client).where(Client.id == order_data.client_id)
    ).first()

    if not client:
        raise error_responses.EXCEPTION_404

    for item in order_data.items:
        check_product_availability_and_stock(item, session)

    db_order = Order(
        client_id=order_data.client_id,
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    for item in order_data.items:
        product = session.exec(
            select(Product).where(Product.barcode == item.product_id)
        ).first()
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity)
        session.add(order_item)
        product.stock -= item.quantity
        product.available = False if product.stock == 0 else product.available

    session.commit()
    return {"order_id": db_order.id}


@router.get("/", response_model=Page[OrderReadWithItems])
async def read_orders(
    session: SessionDep,
    min_creation_date: Optional[date] = Query(None),
    max_creation_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    id: Optional[int] = Query(None),
):
    query = select(Order).distinct()

    if section:
        query = (
            query.join(Order.items)
            .join(OrderItem.product)
            .where(Product.section == section)
        )

    if status:
        query = query.where(Order.status == status)
    if min_creation_date:
        query = query.where(Order.created_at >= min_creation_date)
    if max_creation_date:
        query = query.where(Order.created_at <= max_creation_date)
    if client_id:
        query = query.where(Order.client_id == client_id)
    if id:
        query = query.where(Order.id == id)

    return paginate(session, query)


@router.get("/{id}", response_model=OrderReadWithItems)
async def read_one_order(id: int, session: SessionDep):
    order = session.exec(select(Order).where(
        Order.id == id)).first()
    if not order:
        raise error_responses.EXCEPTION_404
    return order


@router.put("/{id}")
async def update_order(
    id: str,
    status: OrderStatus,
    session: SessionDep
):
    db_order = session.exec(select(Order).where(
        Order.id == id).options(selectinload(Order.items))).first()
    if not db_order:
        raise error_responses.EXCEPTION_404

    if status:
        db_order.status = status
        if status == OrderStatus.CANCELED:
            for item in db_order.items:
                product = session.exec(
                    select(Product).where(Product.barcode == item.product_id)
                ).first()
                product.stock += item.quantity
                product.available = True if product.stock > 0 else False
                session.add(product)

    db_order.updated_at = datetime.now(timezone.utc)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.delete("/{id}", status_code=204)
async def delete_order(id: str, session: SessionDep):
    db_order = session.exec(select(Order).where(
        Order.id == id)).first()
    if not db_order:
        raise error_responses.EXCEPTION_404

    session.delete(db_order)
    session.commit()
    return {"detail": "order deleted successfully"}


add_pagination(router)
