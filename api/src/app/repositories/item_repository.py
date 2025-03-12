from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.envs import PAGINATE_PER_PAGE
from app.exceptions import AlreadyExists
from app.models import Item


class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, item: Item) -> Item:
        db_check = await self.db_session.scalar(
            select(Item).where(Item.name == item.name).limit(1)
        )
        if db_check:
            raise AlreadyExists(db_check)

        self.db_session.add(item)
        await self.db_session.commit()
        return item

    async def count(self, name_like: str | None = None) -> int:
        statement = select(func.count(Item.id))
        if name_like:
            statement = statement.where(Item.name.like(f"%{name_like}%"))
        return await self.db_session.scalar(statement)  # type: ignore

    async def get_all(
        self,
        *,
        fields: list[str] | None = None,
        page: int = 1,
        name_like: str | None = None,
        ids: list[int] | None = None,
    ) -> Sequence[Item]:
        page = int(page)
        if page < 1:
            page = 1

        if fields:
            statement = select(*[getattr(Item, f) for f in fields])
        else:
            statement = select(Item)

        statement = statement.limit(PAGINATE_PER_PAGE).offset(
            (page - 1) * PAGINATE_PER_PAGE
        )
        if name_like:
            statement = statement.where(Item.name.like(f"%{name_like}%"))
        if ids:
            statement = statement.where(Item.id.in_(ids))

        items = await self.db_session.scalars(statement)
        return items.all()

    async def get_by_id(self, id: int) -> Item | None:
        item = await self.db_session.scalar(select(Item).filter(Item.id == id).limit(1))
        return item

    async def update(self, item: Item):
        item.name = item.name.strip()
        db_check = await self.db_session.scalar(
            select(Item).where(func.lower(Item.name) == item.name.lower()).limit(1)
        )
        if db_check and db_check.id != item.id:
            raise AlreadyExists(db_check)

        await self.db_session.commit()
