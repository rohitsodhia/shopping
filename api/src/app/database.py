import contextlib
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.envs import DATABASE_DATABASE, DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USER


class DatabaseSessionManager:
    def __init__(
        self,
        host: str = DATABASE_HOST,
        user: str = DATABASE_USER,
        password: str = DATABASE_PASSWORD,
        database: str = DATABASE_DATABASE,
    ):
        self._engine: AsyncEngine | None = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}/{database}"
        )
        self._sessionmaker: async_sessionmaker | None = async_sessionmaker(
            bind=self._engine, autocommit=False, expire_on_commit=False, autoflush=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DatabaseSessionManager()


async def get_db_session():
    async with session_manager.session() as session:
        yield session


DBSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
