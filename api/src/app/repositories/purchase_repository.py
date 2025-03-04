from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.envs import PAGINATE_PER_PAGE
from app.models import Purchase


class PurchaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, purchase: Purchase):
        self.db_session.add(purchase)
        await self.db_session.commit()
        return purchase

    async def get_all(self, page: int = 1) -> Sequence[Purchase]:
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
        item = await self.db_session.scalar(
            select(Purchase).filter(Purchase.id == id).limit(1)
        )
        return item

    async def update(self, purchase: Purchase):
        self.db_session.add(purchase)
        await self.db_session.commit()
