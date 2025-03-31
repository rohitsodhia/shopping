from fastapi import APIRouter

from app.database import DBSessionDependency
from app.helpers.functions import dict_from_schema
from app.repositories import StoreRepository
from app.stores import schemas

stores = APIRouter(prefix="/stores")


@stores.post(
    "",
    response_model=schemas.StoreResponse,
)
async def add_store(store_input: schemas.StoreInput, db_session: DBSessionDependency):
    store_repository = StoreRepository(db_session)
    store = await store_repository.create(name=store_input.name)

    return {"data": {"store": dict_from_schema(store, schemas.Store)}}


@stores.get(
    "",
    response_model=schemas.ListStoresResponse,
)
async def list_stores(db_session: DBSessionDependency, page: int = 1):
    store_repository = StoreRepository(db_session)

    page = int(page)
    if page < 1:
        page = 1

    stores = await store_repository.get_all()

    return {
        "data": {
            "stores": list(stores),
            "page": page,
            "total": await store_repository.count(),
        },
    }


@stores.patch(
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
