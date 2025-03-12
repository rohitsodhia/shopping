from __future__ import annotations

from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.envs import PAGINATE_PER_PAGE
from app.exceptions import IntegrityError
from app.helpers.functions import parse_integrity_error
from app.models import Purchase


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

    async def bulk_create(self, purchases: list) -> Sequence[Purchase]:
        try:
            purchase_objs = await self.db_session.scalars(
                insert(Purchase).returning(Purchase), purchases
            )
        except Exception as e:
            raise e

        await self.db_session.commit()
        return purchase_objs.all()

    async def get_all(self, page: int = 1) -> Sequence[Purchase]:
        page = int(page)
        if page < 1:
            page = 1

        statement = (
            select(Purchase)
            .limit(PAGINATE_PER_PAGE)
            .offset((page - 1) * PAGINATE_PER_PAGE)
        )
        purchses = await self.db_session.scalars(statement)
        return purchses.all()

    async def get_by_id(self, id: int) -> Purchase | None:
        statement = select(Purchase).filter(Purchase.id == id).limit(1)
        item = await self.db_session.scalar(statement)
        return item

    async def update(self, purchase: Purchase):
        await self.db_session.commit()
