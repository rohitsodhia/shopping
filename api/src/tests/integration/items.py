import pytest
from sqlalchemy import insert

from app.configs import configs
from app.models import Item

pytestmark = pytest.mark.anyio


async def test_add_item_success(authed_client):
    store_name = "test"
    response = await authed_client.post("/items", json={"name": store_name})
    assert response.status_code == 200
    assert response.json()["data"]["item"]["name"] == store_name

    notes = "test"
    response = await authed_client.post(
        "/items", json={"name": store_name, "notes": notes}
    )
    assert response.status_code == 200
    assert response.json()["data"]["item"]["notes"] == notes


async def test_add_item_duplicate(authed_client):
    store_name = "test"
    await authed_client.post("/items", json={"name": store_name})
    response = await authed_client.post("/items", json={"name": store_name})
    assert response.status_code == 422
    assert response.json()["errors"][0]["error"] == "already_exists"


async def test_list_items_success(authed_client, db_session):
    await db_session.execute(insert(Item), [{"name": "test1"}, {"name": "test2"}])
    response = await authed_client.get("/items")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["items"]) == 2
    assert response_body["data"]["total"] == 2
    assert response_body["data"]["items"][0]["name"] == "test1"

    configs.PAGINATE_PER_PAGE = 10
    inserts = [{"name": f"test{i}"} for i in range(3, 13)]
    await db_session.execute(insert(Item), inserts)
    response = await authed_client.get("/items")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["items"]) == 10
    assert response_body["data"]["total"] == 12
    response = await authed_client.get("/items", params={"page": 2})
    response_body = response.json()
    assert len(response_body["data"]["items"]) == 2
    assert response_body["data"]["total"] == 12


async def test_get_item_success(authed_client, db_session):
    item = Item(name="test1")
    db_session.add(item)
    await db_session.flush()

    response = await authed_client.get(f"/items/{item.id}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["item"]["name"] == item.name


async def test_get_item_not_found(authed_client):
    response = await authed_client.get(f"/items/1")
    assert response.status_code == 404


async def test_update_item_success(authed_client, db_session):
    item = Item(name="test1")
    db_session.add(item)
    await db_session.flush()

    response = await authed_client.patch(
        f"/items/{item.id}", json={"name": "test2", "notes": "test"}
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["item"]["name"] == "test2"
    assert response_body["data"]["item"]["notes"] == "test"

    response = await authed_client.patch(
        f"/items/{item.id}", json={"name": "test2", "notes": ""}
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["item"]["name"] == "test2"
    assert response_body["data"]["item"]["notes"] == ""
