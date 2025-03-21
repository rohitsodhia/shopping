import pytest

from app.database import session_manager


@pytest.fixture(scope="function")
async def db_session(db_connection):
    async with session_manager.session() as session:
        yield session
