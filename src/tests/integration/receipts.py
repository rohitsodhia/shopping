import datetime

import pytest
from sqlalchemy import insert

from app.configs import configs
from app.models import Item, Purchase, Receipt, Store

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("notes", (None, "test"))
async def test_add_receipt_success(authed_client, db_session, notes):
    store = Store(name="test1")
    db_session.add(store)
    await db_session.flush()

    date = "2022-01-01"
    response = await authed_client.post(
        "/api/receipts", json={"store_id": store.id, "date": date, "notes": notes}
    )
    assert response.status_code == 200
    assert response.json()["data"]["receipt"]["date"] == date
    assert response.json()["data"]["receipt"]["notes"] == notes


async def test_list_receipts_success(authed_client, db_session):
    store1, store2 = await db_session.scalars(
        insert(Store).returning(Store), [{"name": "test1"}, {"name": "test2"}]
    )

    date = datetime.date(2022, 1, 1)
    await db_session.execute(
        insert(Receipt),
        [
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store2.id, "date": date},
            {"store_id": store2.id, "date": date},
        ],
    )
    response = await authed_client.get("/api/receipts")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["receipts"]) == 6
    assert response_body["data"]["total"] == 6
    assert response_body["data"]["receipts"][0]["date"] == date.isoformat()

    configs.PAGINATE_PER_PAGE = 5
    response = await authed_client.get("/api/receipts")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["receipts"]) == 5
    assert response_body["data"]["total"] == 6
    response = await authed_client.get("/api/receipts", params={"page": 2})
    response_body = response.json()
    assert len(response_body["data"]["receipts"]) == 1
    assert response_body["data"]["total"] == 6


async def test_list_receipts_success_by_store(authed_client, db_session):
    store1, store2, store3 = await db_session.scalars(
        insert(Store).returning(Store),
        [{"name": "test1"}, {"name": "test2"}, {"name": "test3"}],
    )

    date = datetime.date(2022, 1, 1)
    await db_session.execute(
        insert(Receipt),
        [
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store1.id, "date": date},
            {"store_id": store2.id, "date": date},
            {"store_id": store2.id, "date": date},
            {"store_id": store3.id, "date": date},
        ],
    )
    response = await authed_client.get("/api/receipts", params={"store_ids": store1.id})
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["receipts"]) == 4

    response = await authed_client.get(
        "/api/receipts", params={"store_ids": [store1.id, store2.id]}
    )
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["receipts"]) == 6


async def test_get_receipt_success(authed_client, db_session):
    store = Store(name="test1")
    db_session.add(store)
    await db_session.flush()
    receipt = Receipt(store_id=store.id, date=datetime.date(2022, 1, 1))
    db_session.add(receipt)
    await db_session.flush()

    response = await authed_client.get(f"/api/receipts/{receipt.id}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["receipt"]["date"] == receipt.date.isoformat()


async def test_get_receipt_not_found(authed_client):
    response = await authed_client.get("/api/receipts/1")
    assert response.status_code == 404


async def test_get_purcahses_success(authed_client, db_session, receipt_generator):
    receipt, store = await receipt_generator()
    response = await authed_client.get(f"/api/receipts/{receipt.id}/purchases")
    assert response.status_code == 200
    assert len(response.json()["data"]["purchases"]) == 0

    item = Item(name="test")
    db_session.add(item)
    await db_session.flush()
    await db_session.execute(
        insert(Purchase),
        [
            {"receipt_id": receipt.id, "item_id": item.id},
            {"receipt_id": receipt.id, "item_id": item.id},
            {"receipt_id": receipt.id, "item_id": item.id},
            {"receipt_id": receipt.id, "item_id": item.id},
        ],
    )

    response = await authed_client.get(f"/api/receipts/{receipt.id}/purchases")
    assert response.status_code == 200
    assert len(response.json()["data"]["purchases"]) == 4


async def test_update_receipt_success(authed_client, db_session):
    store = Store(name="test1")
    db_session.add(store)
    await db_session.flush()
    receipt = Receipt(store_id=store.id, date=datetime.date(2022, 1, 1))
    db_session.add(receipt)
    await db_session.flush()

    new_date = receipt.date + datetime.timedelta(days=1)
    response = await authed_client.patch(
        f"/api/receipts/{receipt.id}",
        json={"date": new_date.isoformat(), "notes": "test"},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["receipt"]["date"] == new_date.isoformat()
    assert response_body["data"]["receipt"]["notes"] == "test"
