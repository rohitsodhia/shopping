import random

import pytest

from app.models import Item, Purchase

from ..generators import receipt_generator  # noqa: F401  # Test fixture

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("price", (None, random.randint(1, 10)))
async def test_add_purchase_success(
    authed_client, db_session, receipt_generator, price
):
    receipt, store = await receipt_generator()
    item = Item(name="test")
    db_session.add(item)
    await db_session.flush()

    json_body = {"item_id": item.id, "receipt_id": receipt.id}
    if price:
        json_body["price"] = price
    response = await authed_client.post(
        "/api/purchases",
        json=json_body,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["purchase"]["item_id"] == item.id
    assert response_data["data"]["purchase"]["receipt_id"] == receipt.id
    assert response_data["data"]["purchase"]["price"] == price


async def test_add_bulk_purchases_success(authed_client, db_session, receipt_generator):
    receipt, store = await receipt_generator()
    item = Item(name="test")
    db_session.add(item)
    await db_session.flush()
    price = random.randint(1, 10)

    purchases = [{"item_id": item.id, "price": price} for i in range(5)]
    response = await authed_client.post(
        "/api/purchases/bulk",
        json={"receipt_id": receipt.id, "purchases": purchases},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["purchases"]) == 5

    purchases = [{"item_id": item.id, "price": price} for i in range(2)]
    response = await authed_client.post(
        "/api/purchases/bulk",
        json={"receipt_id": receipt.id, "purchases": purchases},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["purchases"]) == 2


async def test_update_purchase_success(authed_client, db_session, receipt_generator):
    receipt, store = await receipt_generator()
    item = Item(name="test")
    db_session.add(item)
    await db_session.flush()
    purchase = Purchase(
        item_id=item.id, receipt_id=receipt.id, price=random.randint(1, 10)
    )
    db_session.add(purchase)
    await db_session.flush()

    new_price = random.randint(1, 10)
    response = await authed_client.patch(
        f"/api/purchases/{purchase.id}",
        json={"price": new_price, "notes": "test"},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["purchase"]["price"] == new_price
    assert response_body["data"]["purchase"]["notes"] == "test"
