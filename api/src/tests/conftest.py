import bcrypt
import pytest
from httpx import ASGITransport, AsyncClient

from app.configs import configs
from app.database import get_db_session, session_manager
from app.main import create_app
from app.models.base import Base


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def app():
    yield create_app(init_db=False)


@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
def set_env_password():
    configs.PASSWORD_HASH = bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode()


@pytest.fixture(scope="function", autouse=True)
async def connection_test():
    session_manager.init(
        host=configs.DATABASE_HOST,
        user=configs.DATABASE_USER,
        password=configs.DATABASE_PASSWORD,
        database=f"{configs.DATABASE_DATABASE}_test",
    )
    yield
    await session_manager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with session_manager.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with session_manager.session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_db_override
