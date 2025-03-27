from fastapi import APIRouter

from app.database import DBSessionDependency
from app.exceptions import AlreadyExists, IntegrityError, NotFound
from app.helpers.functions import dict_from_schema
from app.helpers.response_errors import (
    already_exists_error,
    error_response,
    fields_missing_response,
    integrity_error_response,
    not_found_response,
)
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
        store = await store_repository.create(name=store_input.name)
    except IntegrityError as e:
        return error_response(
            status_code=422, content=[integrity_error_response(str(e))]
        )
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content=[already_exists_error(dict_from_schema(e.cls, schemas.Store))],
        )

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

    try:
        stores = await store_repository.get_all()
    except:
        return error_response(
            status_code=400,
        )

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

    if not store_input.name:
        return fields_missing_response(["name"])

    try:
        store = await store_repository.update(id=store_id, name=store_input.name)
    except NotFound as e:
        return not_found_response()
    except AlreadyExists as e:
        return error_response(
            status_code=400,
            content=[already_exists_error(dict_from_schema(e.cls, schemas.Store))],
        )
    except Exception as e:
        return error_response(
            status_code=400,
        )

    return {
        "data": {
            "store": dict_from_schema(store, schemas.Store),
        },
    }
