from fastapi import APIRouter

from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.helpers.functions import dict_from_schema, error_response
from app.models.store import Store
from app.repositories import StoreRepository
from app.stores import schemas

stores = APIRouter(prefix="/stores")


@stores.post(
    "",
    response_model=schemas.StoreResponse,
)
async def add_store(store_input: schemas.StoreInput, db_session: DBSessionDependency):
    store_repository = StoreRepository(db_session)
    try:
        store = await store_repository.create(Store(name=store_input.name))
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content=[
                {
                    "store": dict_from_schema(e.cls, schemas.Store),
                    "error": "already_exists",
                }
            ],
        )

    if store:
        return {"data": {"store": dict_from_schema(store, schemas.Store)}}


@stores.get(
    "",
    response_model=schemas.ListStoresResponse,
)
async def list_stores(db_session: DBSessionDependency, page: int | None = None):
    store_repository = StoreRepository(db_session)
    if not page or page < 1:
        page = 1
    try:
        stores = await store_repository.get_all()
    except:
        return error_response(
            status_code=400,
        )

    if stores:
        return {
            "data": {
                "stores": list(stores),
                "page": page,
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

    if not store_input.name:
        return error_response(
            status_code=400,
            content=[{"error": "no_data"}],
        )

    try:
        store = await store_repository.get_by_id(store_id)
        if not store:
            return error_response(status_code=404, content=[{"error": "not_found"}])
        store.name = store_input.name
        await store_repository.update(store)
    except Exception as e:
        print(e)
        return error_response(
            status_code=400,
        )

    return {
        "data": {
            "store": dict_from_schema(store, schemas.Store),
        },
    }
