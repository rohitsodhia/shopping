from fastapi import APIRouter

from app import schemas as global_schemas
from app.database import DBSessionDependency
from app.exceptions import NotFound
from app.helpers.functions import dict_from_schema
from app.items import schemas
from app.models import Item
from app.repositories import ItemRepository

items = APIRouter(prefix="/api/items")


@items.post(
    "",
    response_model=schemas.ItemResponse,
    responses={422: {"model": global_schemas.AlreadyExistsResponse}},
)
async def add_item(item_input: schemas.NewItemInput, db_session: DBSessionDependency):
    item_repository = ItemRepository(db_session)
    item = await item_repository.create(name=item_input.name)

    return {"data": {"item": dict_from_schema(item, schemas.Item)}}


@items.get(
    "",
    response_model=schemas.ListItemsResponse,
)
async def list_items(
    db_session: DBSessionDependency, page: int = 1, search: str | None = None
):
    item_repository = ItemRepository(db_session)

    page = int(page)
    if page < 1:
        page = 1

    items = await item_repository.get_all(page=page, name_like=search)

    return {
        "data": {
            "items": list(items),
            "page": page,
            "total": await item_repository.count(name_like=search),
        },
    }


@items.get(
    "/{item_id}",
    response_model=schemas.GetItemResponse,
)
async def get_item(db_session: DBSessionDependency, item_id: int):
    item_repository = ItemRepository(db_session)
    item = await item_repository.get_by_id(item_id)

    if not item:
        raise NotFound(Item)
    return {
        "data": {
            "item": dict_from_schema(item, schemas.Item),
        },
    }


@items.patch(
    "/{item_id}",
    response_model=schemas.GetItemResponse,
)
async def update_item(
    item_id: int, item_input: schemas.ItemInput, db_session: DBSessionDependency
):
    item_repository = ItemRepository(db_session)

    item = await item_repository.update(
        item_id, name=item_input.name, notes=item_input.notes
    )

    return {
        "data": {
            "item": dict_from_schema(item, schemas.Item),
        },
    }
