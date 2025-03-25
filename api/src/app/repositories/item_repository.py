from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import AlreadyExists, IntegrityError, NotFound
from app.helpers.functions import parse_integrity_error
from app.models import Item


class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, name: str) -> Item:
        item = Item(name=name)
        self.db_session.add(item)
        try:
            await self.db_session.commit()
        except SQLAIntegrityError as e:
            if str(e.orig):
                if insert_vals := parse_integrity_error(str(e.orig)):
                    raise IntegrityError(*insert_vals)
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

        statement = statement.limit(configs.PAGINATE_PER_PAGE).offset(
            (page - 1) * configs.PAGINATE_PER_PAGE
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

    async def update(self, id: int, name: str | None = None, notes: str | None = None):
        item = await self.get_by_id(id)
        if not item:
            raise NotFound(Item)

        if name is not None:
            item.name = name.strip()
        if notes is not None:
            item.notes = notes

        db_check = await self.db_session.scalar(
            select(Item).where(func.lower(Item.name) == item.name.lower()).limit(1)
        )
        if db_check and db_check.id != item.id:
            raise AlreadyExists(db_check)

        await self.db_session.commit()
        return item
