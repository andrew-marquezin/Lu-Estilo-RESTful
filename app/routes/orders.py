from typing import Annotated, Optional
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.db import get_session
from app.models.tables import Order


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["orders"])


@router.post("/")
async def create_order(
    order: dict,
    session: SessionDep
):
    db_order = Order(**order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=Page[Order])
async def read_orders(
    session: SessionDep,
    min_creation_date: Optional[date] = Query(None),
    max_creation_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    product_section: Optional[str] = Query(None),
    id: Optional[int] = Query(None),
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)
    if min_creation_date:
        query = query.where(Order.created_at >= min_creation_date)
    if max_creation_date:
        query = query.where(Order.created_at <= max_creation_date)
    if client_id:
        query = query.where(Order.client_id == client_id)
    if product_section:
        query = query.where(Order.product_section == product_section)
    if id:
        query = query.where(Order.id == id)

    return paginate(session, query)


@router.get("/{id}", response_model=Order)
async def read_one_order(id: int, session: SessionDep):
    order = session.exec(select(Order).where(
        Order.id == id)).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="order not found"
        )
    return order


@router.put("/{id}")
async def update_order(
    id: str,
    order: dict,
    session: SessionDep
):
    db_order = session.exec(select(Order).where(
        order.id == id)).first()
    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="order not found"
        )

    for key, value in order.items():
        setattr(db_order, key, value)
    db_order.updated_at = datetime.now(timezone.utc)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.delete("/{id}")
async def delete_order(id: str, session: SessionDep):
    db_order = session.exec(select(Order).where(
        Order.id == id)).first()
    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="order not found"
        )

    session.delete(db_order)
    session.commit()
    return {"detail": "order deleted successfully"}


add_pagination(router)
