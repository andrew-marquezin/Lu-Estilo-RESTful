from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi_pagination import add_pagination, Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from app.db import get_session
from app.models.tables import Client


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(tags=["clients"])


@router.post("/", response_model=Client)
async def create_client(
        client: dict,
        session: SessionDep
):
    db_client = Client(**client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


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


@router.get("/{id}", response_model=Client)
async def read_one_client(id: int, session: SessionDep):
    client = session.exec(select(Client).where(Client.id == id)).first()
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    return client


@router.put("/{id}")
async def update_client(id: int, client: dict, session: SessionDep):
    db_client = session.exec(select(Client).where(Client.id == id)).first()
    if not db_client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    for key, value in client.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


@router.delete("/{id}")
async def delete_client(id: int, session: SessionDep):
    db_client = session.exec(select(Client).where(Client.id == id)).first()
    if not db_client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    session.delete(db_client)
    session.commit()
    return {"detail": "Client deleted successfully"}


add_pagination(router)
