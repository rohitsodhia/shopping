import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import AlreadyExists, NotFound
from app.models.store import Store
from app.repositories.store_repository import StoreRepository

pytestmark = pytest.mark.anyio


class TestStoreRepository:
    async def test_create(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        store = await store_repository.create(name="test")
        assert store.id

        store_from_db = await db_session.scalar(select(Store).limit(1))
        assert store_from_db
        assert store.id == store_from_db.id
        assert store.name == store_from_db.name

    async def test_create_name_with_padding(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        name_with_padding = "test with padding"
        store = await store_repository.create(name=f"{name_with_padding} ")
        assert store.id

        store_from_db = await db_session.scalar(select(Store).limit(1))
        assert store_from_db
        assert store.id == store_from_db.id
        assert store.name == store_from_db.name

    async def test_create_exception_same_name(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        name = "test"
        store = await store_repository.create(name=name)
        with pytest.raises(AlreadyExists) as e:
            await store_repository.create(name=name)
        with pytest.raises(AlreadyExists) as e:
            await store_repository.create(name=name.upper())

    async def test_count(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        await db_session.execute(insert(Store), [{"name": "test1"}, {"name": "test2"}])
        assert await store_repository.count() == 2
        db_session.add(Store(name="test3"))
        await db_session.commit()
        assert await store_repository.count() == 3

    async def test_get_all(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        stores_inserted = await db_session.scalars(
            insert(Store).returning(Store),
            [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}],
        )

        stores_in_db = await store_repository.get_all()
        assert len(stores_in_db) == 3

        configs.PAGINATE_PER_PAGE = 2
        stores_in_db = await store_repository.get_all()
        assert len(stores_in_db) == 2
        stores_in_db = await store_repository.get_all(2)
        assert len(stores_in_db) == 1

    async def test_get_all_invalid_page(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        with pytest.raises(ValueError) as e:
            await store_repository.get_all(0)
        with pytest.raises(ValueError) as e:
            await store_repository.get_all(-1)

    async def test_get_by_id(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        stores_inserted = await db_session.scalars(
            insert(Store).returning(Store), [{"name": "test1"}, {"name": "test2"}]
        )
        store1, store2 = stores_inserted.all()
        store_by_id = await store_repository.get_by_id(store2.id)
        assert store_by_id
        assert store2.name == store_by_id.name

        store_by_id = await store_repository.get_by_id(10)
        assert store_by_id is None

    async def test_update(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()

        store = await store_repository.update(id=store.id, name="test2")
        assert store.name == "test2"

    async def test_update_no_store(self, db_session: AsyncSession):
        store_repository = StoreRepository(db_session)
        with pytest.raises(NotFound) as e:
            await store_repository.update(id=1, name="test")
