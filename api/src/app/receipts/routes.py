from fastapi import APIRouter

from app.database import DBSessionDependency
from app.helpers.functions import dict_from_schema
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

    if receipt:
        return {"data": {"receipt": dict_from_schema(receipt, schemas.Receipt)}}
