import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AlreadyExists
from app.models.store import Store
from app.repositories.store_repository import StoreRepository

pytestmark = pytest.mark.anyio


class TestStoreRepository:
    async def test_create_store_success(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        store = await store_repository.create(name="test")
        assert store.id

        store_from_db = await db_session.scalar(select(Store).limit(1))
        assert store_from_db
        assert store.id == store_from_db.id
        assert store.name == store_from_db.name

    async def test_create_store_success_name_with_padding(
        self, db_session: AsyncSession
    ):
        store_repository = StoreRepository(db_session)
        name_with_padding = "test with padding"
        store = await store_repository.create(name=f"{name_with_padding} ")
        assert store.id

        store_from_db = await db_session.scalar(select(Store).limit(1))
        assert store_from_db
        assert store.id == store_from_db.id
        assert store.name == store_from_db.name

    async def test_create_store_exception_same_name(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        name = "test"
        store = await store_repository.create(name=name)
        with pytest.raises(AlreadyExists) as e:
            store = await store_repository.create(name=name)
        assert store.id
