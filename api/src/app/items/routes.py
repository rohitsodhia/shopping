from fastapi import APIRouter

from app.database import DBSessionDependency
from app.exceptions import AlreadyExists, IntegrityError
from app.helpers.functions import dict_from_schema
from app.helpers.response_errors import (
    already_exists_error,
    error_response,
    fields_missing_response,
    integrity_error_response,
    not_found_response,
)
from app.items import schemas
from app.models.item import Item
from app.repositories import ItemRepository

items = APIRouter(prefix="/items")


@items.post(
    "",
    response_model=schemas.ItemResponse,
)
async def add_item(item_input: schemas.NewItemInput, db_session: DBSessionDependency):
    item_repository = ItemRepository(db_session)
    try:
        item = await item_repository.create(name=item_input.name)
    except IntegrityError as e:
        return error_response(
            status_code=422, content=[integrity_error_response(str(e))]
        )
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content=[already_exists_error(dict_from_schema(e.cls, schemas.Item))],
        )

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
    try:
        item = await item_repository.get_by_id(item_id)
    except:
        return error_response(
            status_code=400,
        )

    if not item:
        return not_found_response()
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
        return fields_missing_response(["name", "notes"])

    try:
        item = await item_repository.update(
            item_id, name=item_input.name, notes=item_input.notes
        )
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content=[already_exists_error(dict_from_schema(e.cls, schemas.Item))],
        )
    except Exception as e:
        return error_response(
            status_code=400,
        )

    return {
        "data": {
            "item": dict_from_schema(item, schemas.Item),
        },
    }
