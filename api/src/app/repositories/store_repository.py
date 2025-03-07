from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.envs import PAGINATE_PER_PAGE
from app.exceptions import AlreadyExists
from app.models import Store


class StoreRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, store: Store):
        store.name = store.name.strip()
        db_check = await self.db_session.scalar(
            select(Store).where(func.lower(Store.name) == store.name.lower()).limit(1)
        )
        if db_check:
            raise AlreadyExists(db_check)

        self.db_session.add(store)
        await self.db_session.commit()
        return store

    async def count(self) -> int:
        return await self.db_session.scalar(select(func.count(Store.id)))  # type: ignore

    async def get_all(self, page: int = 1) -> Sequence[Store]:
        page = int(page)
        if page < 1:
            page = 1

        statement = (
            select(Store)
            .limit(PAGINATE_PER_PAGE)
            .offset((page - 1) * PAGINATE_PER_PAGE)
        )
        stores = await self.db_session.scalars(statement)
        return stores.all()

    async def get_by_id(self, id: int) -> Store | None:
        item = await self.db_session.scalar(
            select(Store).filter(Store.id == id).limit(1)
        )
        return item

    async def update(self, store: Store):
        store.name = store.name.strip()
        db_check = await self.db_session.scalar(
            select(Store).where(func.lower(Store.name) == store.name.lower()).limit(1)
        )
        from icecream import ic

        if db_check and db_check.id != store.id:
            raise AlreadyExists(db_check)

        await self.db_session.commit()
