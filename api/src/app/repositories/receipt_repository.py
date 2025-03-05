from __future__ import annotations

import datetime

from sqlalchemy.ext.asyncio import AsyncSession

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
