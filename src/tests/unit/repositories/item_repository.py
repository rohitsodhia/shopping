import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import AlreadyExists, NotFound
from app.models import Item
from app.repositories import ItemRepository

pytestmark = pytest.mark.anyio


class TestItemRepository:
    async def test_create(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        item = await item_repository.create(name="test")
        assert item.id

        item_from_db = await db_session.scalar(select(Item).limit(1))
        assert item_from_db
        assert item.id == item_from_db.id
        assert item.name == item_from_db.name

    async def test_create_exception_same_name(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        name = "test"
        item = await item_repository.create(name=name)
        with pytest.raises(AlreadyExists) as e:
            await item_repository.create(name=name)

    async def test_count(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        await db_session.execute(insert(Item), [{"name": "test1"}, {"name": "test2"}])
        assert await item_repository.count() == 2
        db_session.add(Item(name="item3"))
        await db_session.commit()
        assert await item_repository.count() == 3

        assert await item_repository.count(name_like="test") == 2

    async def test_get_all(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        items_inserted = await db_session.scalars(
            insert(Item).returning(Item),
            [{"name": "test1"}, {"name": "test2"}, {"name": "item3"}],
        )

        items_in_db = await item_repository.get_all()
        assert len(items_in_db) == 3

        items_in_db = await item_repository.get_all(name_like="test")
        assert len(items_in_db) == 2

        configs.PAGINATE_PER_PAGE = 2
        items_in_db = await item_repository.get_all()
        assert len(items_in_db) == 2
        items_in_db = await item_repository.get_all(2)
        assert len(items_in_db) == 1

    async def test_get_by_id(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        items_inserted = await db_session.scalars(
            insert(Item).returning(Item), [{"name": "test1"}, {"name": "test2"}]
        )
        item1, item2 = items_inserted.all()
        item_by_id = await item_repository.get_by_id(item2.id)
        assert item_by_id
        assert item2.name == item_by_id.name

        item_by_id = await item_repository.get_by_id(10)
        assert item_by_id is None

    async def test_update(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        item = Item(name="test", notes="test")
        db_session.add(item)
        await db_session.commit()

        item = await item_repository.update(id=item.id, name="test2", notes="test more")
        assert item.name == "test2", item.notes == "test more"

        item_from_db = await db_session.scalar(select(Item).limit(1))
        assert item_from_db
        assert item.id == item_from_db.id
        assert item.name == item_from_db.name

    async def test_update_no_item(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        with pytest.raises(NotFound) as e:
            await item_repository.update(id=1, name="test")

    async def test_update_duplicate_item(self, db_session: AsyncSession):
        item_repository = ItemRepository(db_session)
        items_inserted = await db_session.scalars(
            insert(Item).returning(Item), [{"name": "test1"}, {"name": "test2"}]
        )
        item1, item2 = items_inserted.all()

        async with db_session.begin_nested():
            with pytest.raises(AlreadyExists) as e:
                await item_repository.update(id=item2.id, name="test1")
