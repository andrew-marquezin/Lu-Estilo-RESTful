from typing import Annotated, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.auth.dependencies import require_admin
from app.db import get_session
from app.models.tables import Product
from app.models.schemas import ProductCreate, ProductRead
from app.utils import error_responses


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    session: SessionDep,
    user=Depends(require_admin)
):
    existing_product = session.exec(
        select(Product).where(Product.barcode == product.barcode)).first()
    if existing_product:
        raise error_responses.barcode_already_exists(product.barcode)

    db_product = Product(**product.model_dump())

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return {"product_id": db_product.barcode}


@router.get("/", response_model=Page[ProductRead])
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


@router.get("/{barcode}", response_model=ProductRead)
async def read_one_product(barcode: str, session: SessionDep):
    product = session.exec(select(Product).where(
        Product.barcode == barcode)).first()
    if not product:
        raise error_responses.EXCEPTION_404
    return product


@router.put("/{barcode}")
async def update_product(
    barcode: str,
    product: dict,
    session: SessionDep,
    user=Depends(require_admin)
):
    db_product = session.exec(select(Product).where(
        Product.barcode == barcode)).first()
    if not db_product:
        raise error_responses.EXCEPTION_404

    for key, value in product.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/{barcode}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    barcode: str,
    session: SessionDep,
    user=Depends(require_admin)
):
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
