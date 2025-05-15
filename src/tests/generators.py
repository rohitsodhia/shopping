import datetime

import pytest

from app.models import Receipt, Store


@pytest.fixture
async def receipt_generator(db_session):
    async def _receipt_generator(
        store_name: str = "test",
        receipt_date: datetime.date | None = None,
    ) -> tuple[Receipt, Store]:
        if receipt_date is None:
            receipt_date = datetime.date.today()
        store = Store(name=store_name)
        db_session.add(store)
        await db_session.flush()
        receipt = Receipt(store_id=store.id, date=receipt_date)
        db_session.add(receipt)
        await db_session.flush()

        return receipt, store

    return _receipt_generator
