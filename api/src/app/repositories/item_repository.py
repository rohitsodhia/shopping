from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ItemAlreadyExists
from app.models import Item


class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_item(self, item: Item):
        db_check = await self.db_session.scalar(
            select(Item).where(Item.name == item.name).limit(1)
        )
        if db_check:
            item = db_check
            raise ItemAlreadyExists(item)

        self.db_session.add(item)
        await self.db_session.commit()
        return item

