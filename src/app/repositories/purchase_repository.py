from __future__ import annotations

from typing import NotRequired, Sequence, TypedDict

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import AlreadyExists, NotFound
from app.models import Purchase


class PurchaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        item_id: int,
        receipt_id: int,
        price: float | None = None,
        notes: str | None = None,
    ) -> Purchase:
        purchase = Purchase(
            item_id=item_id, receipt_id=receipt_id, price=price, notes=notes
        )
        self.db_session.add(purchase)

        try:
            await self.db_session.commit()
        except SQLAIntegrityError as e:
            await self.db_session.rollback()
            raise AlreadyExists(Purchase)

        return purchase

    async def bulk_create(
        self,
        purchases: list[dict],
    ) -> Sequence[Purchase]:
        try:
            purchase_results = await self.db_session.scalars(
                insert(Purchase).returning(Purchase),
                purchases,
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

    async def update(self, id: int, price: int | None = None, notes: str | None = None):
        purchase = await self.get_by_id(id)
        if not purchase:
            raise NotFound(Purchase)

        if price is not None:
            purchase.price = price
        if notes is not None:
            purchase.notes = notes

        await self.db_session.commit()
        return purchase
