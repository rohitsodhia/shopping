from contextlib import asynccontextmanager
from pathlib import Path
from random import seed

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import exceptions, middleware, route_exceptions
from app.api.auth.routes import auth_api as auth_api_routes
from app.api.items.routes import items_api as items_api_routes
from app.api.purchases.routes import purchases_api as purchases_api_routes
from app.api.receipts.routes import receipts_api as receipts_api_routes
from app.api.stores.routes import stores_api as stores_api_routes
from app.auth.routes import auth as auth_routes
from app.configs import configs, templates
from app.database import get_db_session, session_manager
from app.items.routes import items as items_routes
from app.receipts.routes import receipts as receipts_routes
from app.stores.routes import stores as stores_routes

seed()


async def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


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

    app.mount(
        "/",
        StaticFiles(directory=f"{Path(__file__).parent}/static"),
        name="static",
    )

    app.add_api_route("/", home_page, response_class=HTMLResponse)

    app.include_router(auth_routes)
    app.include_router(items_routes)
    app.include_router(receipts_routes)
    app.include_router(stores_routes)

    app.include_router(auth_api_routes)
    app.include_router(items_api_routes)
    app.include_router(purchases_api_routes)
    app.include_router(receipts_api_routes)
    app.include_router(stores_api_routes)

    return app
