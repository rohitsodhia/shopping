import pytest

from .fixtures import auth_headers

pytestmark = pytest.mark.anyio


async def test_add_item_success(client):
    store_name = "test"
    response = await client.post(
        "/items", headers=auth_headers(), json={"name": store_name}
    )
    assert response.status_code == 200
    assert response.json()["data"]["item"]["name"] == store_name


async def test_add_item_failure_duplicate(client):
    store_name = "test"
    await client.post("/items", headers=auth_headers(), json={"name": store_name})
    response = await client.post(
        "/items", headers=auth_headers(), json={"name": store_name}
    )
    assert response.status_code == 422
    assert response.json()["errors"][0]["error"] == "already_exists"
