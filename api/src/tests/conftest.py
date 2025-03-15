import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.database import get_db_session, session_manager
from app.main import create_app
from app.models.base import Base


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield create_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    host = test_db.host
    port = test_db.port
    user = test_db.user
    db = test_db.dbname
    password = test_db.password

    with DatabaseJanitor(
        user=user,
        host=host,
        port=port,
        dbname=db,
        version=test_db.version,
        password=password,
    ):
        session_manager.init(host=host, user=user, password=password, database=db)
        yield
        await session_manager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with session_manager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with session_manager.session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_db_override
