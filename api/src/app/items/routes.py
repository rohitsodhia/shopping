from fastapi import APIRouter, status

from app.database import DBSessionDependency
from app.exceptions import ItemAlreadyExists
from app.helpers.functions import dict_from_schema, error_response
from app.items import schemas
from app.models.item import Item
from app.repositories import ItemRepository

items = APIRouter(prefix="/items")


@items.post(
    "/",
    response_model=schemas.NewItemResponse,
)
async def add_item(item_input: schemas.NewItemInput, db_session: DBSessionDependency):
    item_repository = ItemRepository(db_session)
    try:
        item = await item_repository.create_item(Item(name=item_input.name))
    except ItemAlreadyExists as e:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "item": dict_from_schema(e.item, schemas.Item),
                "error": "already_exists",
            },
        )

    if item:
        return {
            "data": {
                "item": {
                    "id": item.id,
                    "name": item.name,
                }
            }
        }

