from fastapi import APIRouter

from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.helpers.functions import dict_from_schema, error_response
from app.items import schemas
from app.models.item import Item
from app.repositories import ItemRepository

items = APIRouter(prefix="/items")


@items.post(
    "",
    response_model=schemas.NewItemResponse,
)
async def add_item(item_input: schemas.NewItemInput, db_session: DBSessionDependency):
    item_repository = ItemRepository(db_session)
    try:
        item = await item_repository.create(Item(name=item_input.name))
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content={
                "item": dict_from_schema(e.cls, schemas.Item),
                "error": "already_exists",
            },
        )

    if item:
        return {"data": {"item": dict_from_schema(item, schemas.Item)}}


@items.get(
    "",
    response_model=schemas.ListItemsResponse,
)
async def list_items(
    db_session: DBSessionDependency, page: int | None = None, search: str | None = None
):
    item_repository = ItemRepository(db_session)
    if not page or page < 1:
        page = 1
    try:
        items = await item_repository.get_all(name_like=search)
    except:
        return error_response(
            status_code=400,
        )

    if items:
        return {
            "data": {
                "items": list(items),
                "page": page,
            },
        }


@items.get(
    "/{item_id}",
    response_model=schemas.GetItemResponse,
)
async def get_item(db_session: DBSessionDependency, item_id: int):
    item_repository = ItemRepository(db_session)
    try:
        item = await item_repository.get_by_id(item_id)
    except:
        return error_response(
            status_code=400,
        )

    if not item:
        return error_response(
            status_code=404, content={"not_found": {"details": "Item not found"}}
        )
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

    if not item_input.name and not item_input.notes:
        return error_response(
            status_code=400,
            content={"error": "Nothing to update"},
        )

    try:
        item = await item_repository.get_by_id(item_id)
        if not item:
            return error_response(
                status_code=404, content={"not_found": {"details": "Item not found"}}
            )
        if item_input.name:
            item.name = item_input.name
        if item_input.notes:
            item.notes = item_input.notes
        await item_repository.update(item)
    except Exception as e:
        print(e)
        return error_response(
            status_code=400,
        )

    return {
        "data": {
            "item": dict_from_schema(item, schemas.Item),
        },
    }
