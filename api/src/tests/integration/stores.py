import pytest
from sqlalchemy import insert

from app.configs import configs
from app.models import Store

pytestmark = pytest.mark.anyio


async def test_add_store_success(authed_client):
    store_name = "test"
    response = await authed_client.post("/stores", json={"name": store_name})
    assert response.status_code == 200
    assert response.json()["data"]["store"]["name"] == store_name


async def test_add_store_duplicate(authed_client):
    store_name = "test"
    await authed_client.post("/stores", json={"name": store_name})
    response = await authed_client.post("/stores", json={"name": store_name})
    assert response.status_code == 422
    assert response.json()["errors"][0]["error"] == "already_exists"


async def test_list_stores_success(authed_client, db_session):
    await db_session.execute(insert(Store), [{"name": "test1"}, {"name": "test2"}])
    response = await authed_client.get("/stores")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["stores"]) == 2
    assert response_body["data"]["total"] == 2
    assert response_body["data"]["stores"][0]["name"] == "test1"

    configs.PAGINATE_PER_PAGE = 10
    inserts = [{"name": f"test{i}"} for i in range(3, 13)]
    await db_session.execute(insert(Store), inserts)
    response = await authed_client.get("/stores")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["data"]["stores"]) == 10
    assert response_body["data"]["total"] == 12
    response = await authed_client.get("/stores", params={"page": 2})
    response_body = response.json()
    assert len(response_body["data"]["stores"]) == 2
    assert response_body["data"]["total"] == 12


async def test_update_store_success(authed_client, db_session):
    store = Store(name="test1")
    db_session.add(store)
    await db_session.flush()

    response = await authed_client.patch(f"/stores/{store.id}", json={"name": "test2"})
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["data"]["store"]["name"] == "test2"
