from __future__ import annotations

import datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.envs import PAGINATE_PER_PAGE
from app.models import Receipt


class ReceiptRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self, store_id: int, date: datetime.date | str, notes: str | None = None
    ) -> Receipt:
        receipt = Receipt(store_id=store_id, date=date, notes=notes)
        self.db_session.add(receipt)
        await self.db_session.commit()
        return receipt

    async def count(self, store_ids: int | list[int] | None = None) -> int:
        statement = select(func.count(Receipt.id))
        if type(store_ids) == list:
            store_ids = [int(x) for x in store_ids]
            statement = statement.where(Receipt.store_id.in_(store_ids))
        elif type(store_ids) == int:
            statement = statement.where(Receipt.store_id == store_ids)
        return await self.db_session.scalar(statement)  # type: ignore

    async def get_all(
        self, page: int = 1, store_ids: int | list[int] | None = None
    ) -> Sequence[Receipt]:
        page = int(page)
        if page < 1:
            page = 1

        statement = (
            select(Receipt)
            .limit(PAGINATE_PER_PAGE)
            .offset((page - 1) * PAGINATE_PER_PAGE)
        )
        if type(store_ids) == list and len(store_ids) > 1:
            store_ids = [int(x) for x in store_ids]
            statement = statement.where(Receipt.store_id.in_(store_ids))
        elif type(store_ids) == int or (
            type(store_ids) == list and len(store_ids) == 1
        ):
            if type(store_ids) == list:
                store_ids = store_ids[0]
            statement = statement.where(Receipt.store_id == store_ids)

        receipts = await self.db_session.scalars(statement)
        return receipts.all()

    async def get_by_id(self, id: int) -> Receipt | None:
        receipt = await self.db_session.scalar(
            select(Receipt).filter(Receipt.id == id).limit(1)
        )
        return receipt

    async def update(self, receipt: Receipt):
        await self.db_session.commit()
