import pytest
from sqlalchemy import text

from app.database import session_manager

from .fixtures import auth_headers

pytestmark = pytest.mark.anyio


async def test_add_item_success(client, db_connection):
    store_name = "test"
    response = await client.post(
        "/items", headers=auth_headers(), json={"name": store_name}
    )
    assert response.status_code == 200

    async with session_manager.connect() as connection:
        db_check = await connection.execute(text("SELECT * FROM items LIMIT 1"))
        assert db_check.rowcount == 1

        result = db_check.mappings().one()
        assert result["name"] == store_name
