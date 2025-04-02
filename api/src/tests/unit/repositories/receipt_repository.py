import datetime
import random

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.exceptions import NotFound
from app.models import Receipt, Store
from app.repositories import ReceiptRepository

pytestmark = pytest.mark.anyio


class TestReceiptRepository:
    async def test_create(self, db_session: AsyncSession):
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()

        date = datetime.date.today()
        receipt_repository = ReceiptRepository(db_session)
        receipt = await receipt_repository.create(store_id=store.id, date=date)
        assert receipt.id

        receipt_from_db = await db_session.scalar(select(Receipt).limit(1))
        assert receipt_from_db
        assert receipt.id == receipt_from_db.id
        assert receipt.date == receipt_from_db.date

    async def test_count(self, db_session: AsyncSession):
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()

        date = datetime.date.today()
        await db_session.execute(
            insert(Receipt),
            [
                {"store_id": store.id, "date": date},
                {"store_id": store.id, "date": date},
            ],
        )

        receipt_repository = ReceiptRepository(db_session)
        assert await receipt_repository.count() == 2
        db_session.add(Receipt(store_id=store.id, date=date))
        await db_session.commit()
        assert await receipt_repository.count() == 3

    async def test_count_by_store_id(self, db_session: AsyncSession):
        store1, store2 = await db_session.scalars(
            insert(Store).returning(Store), [{"name": "test1"}, {"name": "test2"}]
        )

        date = datetime.date.today()
        await db_session.execute(
            insert(Receipt),
            [
                {"store_id": store1.id, "date": date},
                {"store_id": store1.id, "date": date},
                {"store_id": store2.id, "date": date},
            ],
        )

        receipt_repository = ReceiptRepository(db_session)
        assert await receipt_repository.count(store_ids=store1.id) == 2
        assert await receipt_repository.count(store_ids=[store2.id]) == 1
        assert await receipt_repository.count(store_ids=[store1.id, store2.id]) == 3

    async def test_get_all(self, db_session: AsyncSession):
        store1, store2 = await db_session.scalars(
            insert(Store).returning(Store), [{"name": "test1"}, {"name": "test2"}]
        )
        receipt_repository = ReceiptRepository(db_session)
        date = datetime.date.today()
        await db_session.execute(
            insert(Receipt),
            [
                {"store_id": store1.id, "date": date},
                {"store_id": store1.id, "date": date},
                {"store_id": store2.id, "date": date},
            ],
        )
        assert len(await receipt_repository.get_all()) == 3

        assert len(await receipt_repository.get_all(store_ids=store1.id)) == 2
        assert len(await receipt_repository.get_all(store_ids=[store2.id])) == 1
        assert (
            len(await receipt_repository.get_all(store_ids=[store1.id, store2.id])) == 3
        )

        configs.PAGINATE_PER_PAGE = 2
        receipts_in_db = await receipt_repository.get_all()
        assert len(receipts_in_db) == 2
        receipts_in_db = await receipt_repository.get_all(2)
        assert len(receipts_in_db) == 1

    async def test_get_by_id(self, db_session: AsyncSession):
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()

        receipt_repository = ReceiptRepository(db_session)
        date = datetime.date.today()
        receipts_inserted = await db_session.scalars(
            insert(Receipt).returning(Receipt),
            [
                {"store_id": store.id, "date": date},
                {
                    "store_id": store.id,
                    "date": date + datetime.timedelta(days=random.randint(1, 5)),
                },
            ],
        )
        receipt1, receipt2 = receipts_inserted.all()
        receipt_by_id = await receipt_repository.get_by_id(receipt2.id)
        assert receipt_by_id
        assert receipt2.date == receipt_by_id.date

        receipt_by_id = await receipt_repository.get_by_id(10)
        assert receipt_by_id is None

    async def test_update(self, db_session: AsyncSession):
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()

        receipt_repository = ReceiptRepository(db_session)
        date = datetime.date.today()
        receipt = Receipt(store_id=store.id, date=date, notes="test")
        db_session.add(receipt)
        await db_session.commit()

        receipt = await receipt_repository.update(
            id=receipt.id, date=date + datetime.timedelta(days=1), notes="test more"
        )
        assert receipt.date == date + datetime.timedelta(days=1), (
            receipt.notes == "test more"
        )

        receipt_from_db = await db_session.scalar(select(Receipt).limit(1))
        assert receipt_from_db
        assert receipt.id == receipt_from_db.id
        assert receipt.date == receipt_from_db.date

    async def test_update_no_receipt(self, db_session: AsyncSession):
        receipt_repository = ReceiptRepository(db_session)
        with pytest.raises(NotFound) as e:
            await receipt_repository.update(id=1, date=datetime.date.today())
