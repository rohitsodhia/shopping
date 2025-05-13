from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.configs import templates
from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.repositories import StoreRepository

stores = APIRouter(prefix="/stores")


@stores.get("", response_class=HTMLResponse)
async def list_stores(
    request: Request, db_session: DBSessionDependency, page: int = 1, duplicate: int = 0
):
    store_repository = StoreRepository(db_session)
    stores = await store_repository.get_all(page=page)

    return templates.TemplateResponse(
        request=request,
        name="stores.html",
        context={"duplicate": duplicate, "stores": stores},
    )


@stores.post("", response_class=RedirectResponse)
async def process_new_store(
    request: Request, db_session: DBSessionDependency, name: Annotated[str, Form()]
):
    store_repository = StoreRepository(db_session)
    try:
        await store_repository.create(name=name)
    except AlreadyExists:
        return RedirectResponse(url="/stores?duplicate=1", status_code=302)

    return RedirectResponse(url="/stores", status_code=302)


@stores.get("/{store_id}", response_class=HTMLResponse)
async def edit_store(
    request: Request, db_session: DBSessionDependency, store_id: int, duplicate: int = 0
):
    store_repository = StoreRepository(db_session)
    store = await store_repository.get_by_id(store_id)

    return templates.TemplateResponse(
        request=request,
        name="store_edit.html",
        context={"store": store, "duplicate": duplicate},
    )


@stores.post("/{store_id}", response_class=RedirectResponse)
async def process_edit_store(
    request: Request,
    db_session: DBSessionDependency,
    store_id: int,
    name: Annotated[str, Form()],
):
    store_repository = StoreRepository(db_session)
    try:
        await store_repository.update(id=store_id, name=name)
    except AlreadyExists:
        return RedirectResponse(url=f"/stores/{store_id}?duplicate=1", status_code=302)

    return RedirectResponse(url="/stores", status_code=302)
