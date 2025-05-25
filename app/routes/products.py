from typing import Annotated, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.db import get_session
from app.models.tables import Product


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["products"])


@router.post("/")
async def create_product(
    product: dict,
    session: SessionDep
):
    db_product = Product(**product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.get("/", response_model=Page[Product])
async def read_products(
    session: SessionDep,
    category: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    available: Optional[bool] = None,
):
    query = select(Product)

    if category:
        query = query.where(Product.category == category)
    if min_price:
        query = query.where(Product.price >= min_price)
    if max_price:
        query = query.where(Product.price <= max_price)
    if available:
        query = query.where(Product.available == available)

    return paginate(session, query)


@router.get("/{barcode}", response_model=Product)
async def read_one_product(barcode: str, session: SessionDep):
    product = session.exec(select(Product).where(
        Product.barcode == barcode)).first()
    if not Product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product


@router.put("/{barcode}")
async def update_product(
    barcode: str,
    product: dict,
    session: SessionDep
):
    db_product = session.exec(select(Product).where(
        Product.barcode == barcode)).first()
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for key, value in product.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/{barcode}")
async def delete_product(barcode: str, session: SessionDep):
    db_product = session.exec(select(Product).where(
        Product.barcode == barcode)).first()
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    session.delete(db_product)
    session.commit()
    return {"detail": "Product deleted successfully"}


add_pagination(router)
