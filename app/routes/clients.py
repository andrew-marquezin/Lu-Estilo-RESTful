from typing import Optional, Annotated

from fastapi import APIRouter, Query, Depends, status
from fastapi_pagination import add_pagination, Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.utils import error_responses
from app.db import get_session
from app.models.tables import Client
from app.models.schemas import (CreateClient,
                                ClientWithOrders)


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["clients"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(
        client: CreateClient,
        session: SessionDep
):
    if client.name == "" or client.email == "" or client.cpf == "":
        raise error_responses.EXCEPTION_422

    existing_client = session.exec(
        select(Client).where(Client.email == client.email)).first()
    if existing_client:
        raise error_responses.email_already_exists(client.email)

    existing_client = session.exec(
        select(Client).where(Client.cpf == client.cpf)).first()
    if existing_client:
        raise error_responses.cpf_already_exists(client.cpf)

    db_client = Client(
        name=client.name,
        email=client.email,
        cpf=client.cpf
    )

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return {"client_id": db_client.id}


@router.get("/", response_model=Page[Client])
async def read_clients(
    session: SessionDep,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    query = select(Client)

    if name:
        query = query.where(Client.name.contains(name))
    if email:
        query = query.where(Client.email.contains(email))

    return paginate(session, query)


@router.get("/{id}", response_model=ClientWithOrders)
async def read_one_client(id: int, session: SessionDep):
    client = session.exec(
        select(Client).where(Client.id == id).options(
            selectinload(Client.orders)
        )
    ).first()
    if not client:
        raise error_responses.EXCEPTION_404
    return client


@router.put("/{id}")
async def update_client(id: int, client: dict, session: SessionDep):
    db_client = session.exec(select(Client).where(Client.id == id)).first()
    if not db_client:
        raise error_responses.EXCEPTION_404

    for key, value in client.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id: int, session: SessionDep):
    db_client = session.exec(
        select(Client).where(Client.id == id)).first()
    if not db_client:
        raise error_responses.EXCEPTION_404

    session.delete(db_client)
    session.commit()
    return

add_pagination(router)
