from fastapi import APIRouter

from app.api.stores import schemas
from app.database import DBSessionDependency
from app.helpers.functions import dict_from_schema
from app.repositories import StoreRepository

stores_api = APIRouter(prefix="/api/stores")


@stores_api.post(
    "",
    response_model=schemas.StoreResponse,
)
async def add_store(store_input: schemas.StoreInput, db_session: DBSessionDependency):
    store_repository = StoreRepository(db_session)
    store = await store_repository.create(name=store_input.name)

    return {"data": {"store": dict_from_schema(store, schemas.Store)}}


@stores_api.get(
    "",
    response_model=schemas.ListStoresResponse,
)
async def list_stores(db_session: DBSessionDependency, page: int = 1):
    store_repository = StoreRepository(db_session)

    page = int(page)
    if page < 1:
        page = 1

    stores = await store_repository.get_all(page=page)

    return {
        "data": {
            "stores": list(stores),
            "page": page,
            "total": await store_repository.count(),
        },
    }


@stores_api.patch(
    "/{store_id}",
    response_model=schemas.StoreResponse,
)
async def update_store(
    store_id: int, store_input: schemas.StoreInput, db_session: DBSessionDependency
):
    store_repository = StoreRepository(db_session)

    store = await store_repository.update(id=store_id, name=store_input.name)

    return {
        "data": {
            "store": dict_from_schema(store, schemas.Store),
        },
    }
