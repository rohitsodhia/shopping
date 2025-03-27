from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import AlreadyExists, IntegrityError, NotFound
from app.helpers.functions import parse_integrity_error
from app.models import Store


class StoreRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, name: str):
        name = name.strip()

        store = Store(name=name)
        self.db_session.add(store)
        try:
            await self.db_session.commit()
        except SQLAIntegrityError as e:
            await self.db_session.rollback()
            raise AlreadyExists(e)
        return store

    async def count(self) -> int:
        return await self.db_session.scalar(select(func.count(Store.id)))  # type: ignore

    async def get_all(self, page: int = 1) -> Sequence[Store]:
        page = int(page)
        if page < 1:
            raise ValueError("page must be an integer greater than or equal to 1")

        statement = (
            select(Store)
            .limit(configs.PAGINATE_PER_PAGE)
            .offset((page - 1) * configs.PAGINATE_PER_PAGE)
        )
        stores = await self.db_session.scalars(statement)
        return stores.all()

    async def get_by_id(self, id: int) -> Store | None:
        item = await self.db_session.scalar(
            select(Store).filter(Store.id == id).limit(1)
        )
        return item

    async def update(self, id: int, name: str) -> Store:
        store = await self.get_by_id(id)
        if not store:
            raise NotFound(Store)

        if name.strip() == store.name:
            return store
        store.name = name.strip()

        try:
            await self.db_session.commit()
        except SQLAIntegrityError as e:
            await self.db_session.rollback()
            raise AlreadyExists(e)
        return store
