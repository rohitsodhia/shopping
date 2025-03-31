from typing import Annotated

from fastapi import APIRouter, Query

from app.database import DBSessionDependency
from app.exceptions import NotFound
from app.helpers.functions import dict_from_schema
from app.models import Receipt
from app.receipts import schemas
from app.repositories import ReceiptRepository

receipts = APIRouter(prefix="/receipts")


@receipts.post(
    "",
    response_model=schemas.ReceiptResponse,
)
async def add_receipt(
    receipt_input: schemas.NewReceiptInput, db_session: DBSessionDependency
):
    receipt_repository = ReceiptRepository(db_session)

    receipt = await receipt_repository.create(
        store_id=receipt_input.store_id,
        date=receipt_input.date,
        notes=receipt_input.notes,
    )

    return {"data": {"receipt": dict_from_schema(receipt, schemas.Receipt)}}


@receipts.get(
    "",
    response_model=schemas.ListReceiptsResponse,
)
async def list_receipts(
    db_session: DBSessionDependency,
    page: int | None = None,
    store_ids: Annotated[list[int] | None, Query()] = None,
):
    receipt_repository = ReceiptRepository(db_session)
    if not page or page < 1:
        page = 1

    receipts = await receipt_repository.get_all(store_ids=store_ids)

    if receipts:
        return {
            "data": {
                "receipts": list(receipts) or [],
                "page": page,
                "total": await receipt_repository.count(store_ids=store_ids),
            },
        }


@receipts.get(
    "/{receipt_id}",
    response_model=schemas.ReceiptResponse,
)
async def get_receipt(db_session: DBSessionDependency, receipt_id: int):
    receipt_repository = ReceiptRepository(db_session)
    receipt = await receipt_repository.get_by_id(receipt_id)

    if not receipt:
        raise NotFound(Receipt)
    return {
        "data": {
            "item": dict_from_schema(receipt, schemas.Receipt),
        },
    }


@receipts.patch(
    "/{receipt_id}",
    response_model=schemas.ReceiptResponse,
)
async def update_receipt(
    receipt_id: int,
    receipt_input: schemas.UpdateReceiptInput,
    db_session: DBSessionDependency,
):
    receipt_repository = ReceiptRepository(db_session)

    receipt = await receipt_repository.update(
        id=receipt_id, date=receipt_input.date, notes=receipt_input.notes
    )

    return {
        "data": {
            "receipt": dict_from_schema(receipt, schemas.Receipt),
        },
    }
