from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.configs import templates
from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.repositories import ItemRepository

items = APIRouter(prefix="/items")


@items.get("", response_class=HTMLResponse)
async def list_items(
    request: Request, db_session: DBSessionDependency, page: int = 1, duplicate: int = 0
):
    item_repository = ItemRepository(db_session)
    items = await item_repository.get_all(page=page)

    return templates.TemplateResponse(
        request=request,
        name="items.html",
        context={"duplicate": duplicate, "items": items},
    )


@items.post("", response_class=RedirectResponse)
async def process_new_item(
    request: Request, db_session: DBSessionDependency, name: Annotated[str, Form()]
):
    item_repository = ItemRepository(db_session)
    try:
        await item_repository.create(name=name)
    except AlreadyExists:
        return RedirectResponse(url="/items?duplicate=1", status_code=302)

    return RedirectResponse(url="/items", status_code=302)


@items.get("/{item_id}", response_class=HTMLResponse)
async def edit_item(
    request: Request, db_session: DBSessionDependency, item_id: int, duplicate: int = 0
):
    item_repository = ItemRepository(db_session)
    item = await item_repository.get_by_id(item_id)

    return templates.TemplateResponse(
        request=request,
        name="item_edit.html",
        context={"item": item, "duplicate": duplicate},
    )


@items.post("/{item_id}", response_class=RedirectResponse)
async def process_edit_item(
    request: Request,
    db_session: DBSessionDependency,
    item_id: int,
    name: Annotated[str, Form()],
    notes: Annotated[str, Form()],
):
    item_repository = ItemRepository(db_session)
    try:
        await item_repository.update(id=item_id, name=name, notes=notes)
    except AlreadyExists:
        return RedirectResponse(url=f"/items/{item_id}?duplicate=1", status_code=302)

    return RedirectResponse(url="/items", status_code=302)
