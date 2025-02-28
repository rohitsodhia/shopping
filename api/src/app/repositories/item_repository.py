from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.envs import PAGINATE_PER_PAGE
from app.exceptions import AlreadyExists
from app.models import Item


class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, item: Item):
        db_check = await self.db_session.scalar(
            select(Item).where(Item.name == item.name).limit(1)
        )
        if db_check:
            item = db_check
            raise AlreadyExists(item)

        self.db_session.add(item)
        await self.db_session.commit()
        return item

    async def get_all(
        self, page: int = 1, name_like: str | None = None
    ) -> Sequence[Item]:
        if page < 1:
            page = 1
        statement = (
            select(Item).limit(PAGINATE_PER_PAGE).offset((page - 1) * PAGINATE_PER_PAGE)
        )
        if name_like:
            statement = statement.where(Item.name.like(f"%{name_like}%"))

        items = await self.db_session.scalars(statement)
        return items.all()

    async def get_by_id(self, id: int) -> Item | None:
        item = await self.db_session.scalar(select(Item).filter(Item.id == id).limit(1))
        return item

    async def update(self, item: Item):
        self.db_session.add(item)
        await self.db_session.commit()
