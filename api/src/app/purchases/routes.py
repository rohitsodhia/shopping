from fastapi import APIRouter

from app.database import DBSessionDependency
from app.helpers.functions import dict_from_schema
from app.models import Purchase
from app.purchases import schemas
from app.repositories import PurchaseRepository

purchases = APIRouter(prefix="/purchases")


@purchases.post(
    "",
    response_model=schemas.NewPurchaseResponse,
)
async def add_purchase(
    purchase_input: schemas.NewPurchaseInput, db_session: DBSessionDependency
):
    purchase_repository = PurchaseRepository(db_session)

    purchase = await purchase_repository.create(
        item_id=purchase_input.item_id,
        receipt_id=purchase_input.receipt_id,
        price=purchase_input.price,
        notes=purchase_input.notes,
    )

    return {"data": {"purchase": dict_from_schema(purchase, schemas.Purchase)}}


@purchases.post(
    "/bulk",
    response_model=schemas.NewPurchaseBulkResponse,
)
async def add_purchase_bulk(
    purchase_input: schemas.NewPurchaseBulkInput, db_session: DBSessionDependency
):
    purchase_repository = PurchaseRepository(db_session)

    purchases_data: list[dict] = []
    for purchase in purchase_input.purchases:
        purchases_data.append(
            {
                **dict_from_schema(purchase, schemas.NewPurchaseBulkPurchaseInput),
                "receipt_id": purchase_input.receipt_id,
            }
        )

    purchases = await purchase_repository.bulk_create(purchases_data)
    return {
        "data": {
            "purchases": [dict_from_schema(p, schemas.Purchase) for p in purchases]
        }
    }


@purchases.patch(
    "/{purchase_id}",
    response_model=schemas.UpdatePurchaseResponse,
)
async def update_purchase(
    purchase_id: int,
    purchase_input: schemas.UpdatePurchaseInput,
    db_session: DBSessionDependency,
):
    purchase_repository = PurchaseRepository(db_session)

    purchase = await purchase_repository.update(
        purchase_id, price=purchase_input.price, notes=purchase_input.notes
    )

    return {
        "data": {
            "purchase": dict_from_schema(purchase, schemas.Purchase),
        },
    }
