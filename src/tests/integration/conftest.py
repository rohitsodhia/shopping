import pytest
from httpx import ASGITransport, AsyncClient

from app.auth.functions import generate_token


@pytest.fixture
async def authed_client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {generate_token()}"},
    ) as ac:
        yield ac
