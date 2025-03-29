from __future__ import annotations

from typing import NotRequired, Sequence, TypedDict

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import IntegrityError, NotFound
from app.helpers.functions import parse_integrity_error
from app.models import Purchase

PurchaseDict = TypedDict(
    "PurchaseDict",
    {
        "item_id": int,
        "receipt_id": int,
        "price": float,
        "notes": NotRequired[str],
    },
)


class PurchaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self, item_id: int, receipt_id: int, price: float, notes: str | None = None
    ) -> Purchase:
        purchase = Purchase(
            item_id=item_id, receipt_id=receipt_id, price=price, notes=notes
        )
        self.db_session.add(purchase)

        try:
            await self.db_session.commit()
        except SQLAIntegrityError as e:
            if str(e.orig):
                if insert_vals := parse_integrity_error(str(e.orig)):
                    raise IntegrityError(*insert_vals)

        return purchase

    async def bulk_create(
        self,
        purchases: list[PurchaseDict],
    ) -> Sequence[Purchase]:
        purchase_objs: list[Purchase] = []
        for purchase in purchases:
            purchase_objs.append(Purchase(**purchase))
        try:
            purchase_results = await self.db_session.scalars(
                insert(Purchase).returning(Purchase),
                [o.__dict__ for o in purchase_objs],
            )
        except Exception as e:
            raise e

        return purchase_results.all()

    async def get_all(self, page: int = 1) -> Sequence[Purchase]:
        statement = (
            select(Purchase)
            .limit(configs.PAGINATE_PER_PAGE)
            .offset((page - 1) * configs.PAGINATE_PER_PAGE)
        )
        purchses = await self.db_session.scalars(statement)
        return purchses.all()

    async def get_by_id(self, id: int) -> Purchase | None:
        statement = select(Purchase).filter(Purchase.id == id).limit(1)
        item = await self.db_session.scalar(statement)
        return item

    async def update(
        self, id: int, price: float | None = None, notes: str | None = None
    ):
        purchase = await self.get_by_id(id)
        if not purchase:
            raise NotFound(Purchase)

        if price is not None:
            purchase.price = price
        if notes is not None:
            purchase.notes = notes

        await self.db_session.commit()
        return purchase
