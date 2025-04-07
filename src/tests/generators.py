import datetime

import pytest

from app.models import Item, Receipt, Store


@pytest.fixture
async def receipt_generator(db_session):
    async def _receipt_generator(
        receipt_date: datetime.date, store_name="test"
    ) -> tuple[Receipt, Store]:
        store = Store(name="test")
        db_session.add(store)
        await db_session.flush()
        receipt = Receipt(store_id=store.id, date=receipt_date)
        db_session.add(receipt)
        await db_session.flush()

        return receipt, store

    return _receipt_generator
