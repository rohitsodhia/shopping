from contextlib import asynccontextmanager
from random import seed

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import exceptions, middleware, route_exceptions
from app.api.auth.routes import auth
from app.api.items.routes import items
from app.api.purchases.routes import purchases
from app.api.receipts.routes import receipts
from app.api.stores.routes import stores
from app.configs import configs
from app.database import get_db_session, session_manager

seed()


def create_app(init_db=True) -> FastAPI:
    if init_db:
        session_manager.init(
            host=configs.DATABASE_HOST,
            user=configs.DATABASE_USER,
            password=configs.DATABASE_PASSWORD,
            database=configs.DATABASE_DATABASE,
        )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if init_db and session_manager._engine is not None:
            await session_manager.close()

    app = FastAPI(
        dependencies=[
            Depends(middleware.validate_jwt),
            Depends(get_db_session),
            Depends(middleware.check_authorization),
        ],
        lifespan=lifespan,
    )

    app.exception_handlers = {
        exceptions.AlreadyExists: route_exceptions.already_exists_exception_handler,
        exceptions.NotFound: route_exceptions.not_found_exception_handler,
    }

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    app.include_router(auth)
    app.include_router(items)
    app.include_router(purchases)
    app.include_router(stores)
    app.include_router(receipts)

    return app
