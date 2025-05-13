import pytest

pytestmark = pytest.mark.anyio


async def test_login_success(client):
    response = await client.post("/api/auth/login", json={"password": "test123"})
    assert response.status_code == 200


async def test_login_wrong_password(client):
    response = await client.post("/api/auth/login", json={"password": "wrong_password"})
    assert response.status_code == 422
