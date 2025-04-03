import datetime
import random

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import configs
from app.models import Item, Purchase, Receipt, Store
from app.repositories import PurchaseRepository

pytestmark = pytest.mark.anyio


class TestPurchaseRepository:
    async def test_create(self, db_session: AsyncSession):
        item = Item(name="test")
        db_session.add(item)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()
        receipt = Receipt(date=datetime.date.today(), store_id=store.id)
        db_session.add(receipt)
        await db_session.commit()

        purchase_repository = PurchaseRepository(db_session)
        price = random.randint(1, 10)
        purchase = await purchase_repository.create(
            item_id=item.id, receipt_id=receipt.id, price=price
        )
        assert purchase.id

        purchase_from_db = await db_session.get(Purchase, purchase.id)
        assert purchase_from_db
        assert purchase.id == purchase_from_db.id
        assert purchase.price == purchase_from_db.price

        purchase_repository = PurchaseRepository(db_session)
        purchase = await purchase_repository.create(
            item_id=item.id, receipt_id=receipt.id, price=price, notes="test"
        )
        assert purchase.id

        purchase_from_db = await db_session.get(Purchase, purchase.id)
        assert purchase_from_db
        assert purchase.id == purchase_from_db.id
        assert purchase.notes == purchase_from_db.notes

    async def test_bulk_create(self, db_session: AsyncSession):
        item = Item(name="test")
        db_session.add(item)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()
        receipt = Receipt(date=datetime.date.today(), store_id=store.id)
        db_session.add(receipt)
        await db_session.commit()

        purchase_repository = PurchaseRepository(db_session)
        price1 = random.randint(1, 10)
        price2 = random.randint(1, 10)
        purchase1, purchase2 = await purchase_repository.bulk_create(
            [
                {"item_id": item.id, "receipt_id": receipt.id, "price": price1},
                {
                    "item_id": item.id,
                    "receipt_id": receipt.id,
                    "price": price2,
                    "notes": "test",
                },
            ]
        )

        assert purchase1.id, purchase2.id

    async def test_get_all(self, db_session: AsyncSession):
        item = Item(name="test")
        db_session.add(item)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()
        receipt = Receipt(date=datetime.date.today(), store_id=store.id)
        db_session.add(receipt)
        await db_session.commit()

        purchase_repository = PurchaseRepository(db_session)
        purchases_inserted = await db_session.scalars(
            insert(Purchase).returning(Purchase),
            [
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
            ],
        )

        purchases_in_db = await purchase_repository.get_all()
        assert len(purchases_in_db) == 3

        configs.PAGINATE_PER_PAGE = 2
        purchases_in_db = await purchase_repository.get_all()
        assert len(purchases_in_db) == 2
        purchases_in_db = await purchase_repository.get_all(2)
        assert len(purchases_in_db) == 1

    async def test_get_by_id(self, db_session: AsyncSession):
        item = Item(name="test")
        db_session.add(item)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()
        receipt = Receipt(date=datetime.date.today(), store_id=store.id)
        db_session.add(receipt)
        await db_session.commit()

        purchase_repository = PurchaseRepository(db_session)
        purchases_inserted = await db_session.scalars(
            insert(Purchase).returning(Purchase),
            [
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
                {"item_id": item.id, "receipt_id": receipt.id, "price": 1},
            ],
        )
        purchase1, purchase2, purchase3 = purchases_inserted.all()

        purchase_by_id = await purchase_repository.get_by_id(purchase2.id)
        assert purchase_by_id
        assert purchase2.price == purchase_by_id.price

        purchase_by_id = await purchase_repository.get_by_id(10)
        assert purchase_by_id is None

    async def test_update(self, db_session: AsyncSession):
        item = Item(name="test")
        db_session.add(item)
        store = Store(name="test")
        db_session.add(store)
        await db_session.commit()
        receipt = Receipt(date=datetime.date.today(), store_id=store.id)
        db_session.add(receipt)
        await db_session.commit()
        price = random.randint(1, 10)
        purchase = Purchase(
            item_id=item.id, receipt_id=receipt.id, price=price, notes="test"
        )
        db_session.add(purchase)
        await db_session.commit()

        purchase_repository = PurchaseRepository(db_session)
        new_price = random.randint(1, 10)
        purchase = await purchase_repository.update(
            id=purchase.id, price=new_price, notes="test more"
        )
        assert purchase.price == new_price, purchase.notes == "test more"

        purchase_from_db = await db_session.get(Purchase, purchase.id)
        assert purchase_from_db
        assert purchase.id == purchase_from_db.id
        assert purchase.price == purchase_from_db.price
