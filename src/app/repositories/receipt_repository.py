from __future__ import annotations

import datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload

from app.configs import configs
from app.exceptions import NotFound
from app.models import Receipt, Store


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
        if type(store_ids) is list:
            store_ids = [int(x) for x in store_ids]
            statement = statement.where(Receipt.store_id.in_(store_ids))
        elif type(store_ids) is int:
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
            .join(Receipt.store)
            .options(contains_eager(Receipt.store))
            .limit(configs.PAGINATE_PER_PAGE)
            .offset((page - 1) * configs.PAGINATE_PER_PAGE)
            .order_by(Receipt.date.desc(), Store.name)
        )
        if type(store_ids) is list and len(store_ids) > 1:
            store_ids = [int(x) for x in store_ids]
            statement = statement.where(Receipt.store_id.in_(store_ids))
        elif type(store_ids) is int or (
            type(store_ids) is list and len(store_ids) == 1
        ):
            if type(store_ids) is list:
                store_ids = store_ids[0]
            statement = statement.where(Receipt.store_id == store_ids)

        receipts = await self.db_session.scalars(statement)
        return receipts.all()

    async def get_by_id(
        self, id: int, with_store: bool = False, with_purchases: bool = False
    ) -> Receipt | None:
        statement = select(Receipt).filter(Receipt.id == id).limit(1)
        if with_store:
            statement = statement.options(joinedload(Receipt.store))
        if with_purchases:
            statement = statement.options(joinedload(Receipt.purchases))
        receipt = await self.db_session.scalar(statement)
        return receipt

    async def update(
        self, id: int, date: datetime.date | None = None, notes: str | None = ""
    ):
        receipt = await self.get_by_id(id)
        if not receipt:
            raise NotFound(Receipt)

        if date:
            receipt.date = date
        if notes:
            receipt.notes = notes

        await self.db_session.commit()
        return receipt
