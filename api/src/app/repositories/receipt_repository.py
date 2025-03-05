from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Receipt


class ReceiptRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, **kwargs):
        receipt = Receipt(**kwargs)
        self.db_session.add(receipt)
        await self.db_session.commit()
        return receipt
