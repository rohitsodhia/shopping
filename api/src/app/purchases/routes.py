from fastapi import APIRouter

from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.helpers.functions import dict_from_schema, error_response
from app.models import Purchase, Store
from app.purchases import schemas
from app.repositories import ItemRepository, PurchaseRepository, StoreRepository

purchases = APIRouter(prefix="/purchases")


@purchases.post(
    "",
    response_model=schemas.NewPurchaseResponse,
)
async def add_purchase(
    purchase_input: schemas.NewPurchaseInput, db_session: DBSessionDependency
):
    purchase_repository = PurchaseRepository(db_session)

    try:
        purchase = await purchase_repository.create(
            item_id=purchase_input.item_id,
            receipt_id=purchase_input.receipt_id,
            price=purchase_input.price,
            notes=purchase_input.notes,
        )
    except IntegrityError as e:
        return error_response(
            status_code=422, content=[integrity_error_response(str(e))]
        )

    return {"data": {"purchase": dict_from_schema(purchase, schemas.Purchase)}}


@purchases.patch(
    "/{purchase_id}",
    response_model=schemas.UpdatePurchaseResponse,
)
async def update_purchase(
    purchase_id: int,
    purchase_input: schemas.PurchaseInput,
    db_session: DBSessionDependency,
):
    purchase_repository = PurchaseRepository(db_session)

    try:
        purchase = await purchase_repository.get_by_id(purchase_id, get_store=True)
        if not purchase:
            return error_response(
                status_code=404,
                content={"not_found": {"details": "Purchase not found"}},
            )
        if purchase_input.price:
            purchase.price = purchase_input.price
        purchase.notes = purchase_input.notes
        await purchase_repository.update(purchase)
    except Exception as e:
        print(e)
        return error_response(
            status_code=400,
        )

    return {
        "data": {
            "purchase": dict_from_schema(purchase, schemas.Purchase),
        },
    }
