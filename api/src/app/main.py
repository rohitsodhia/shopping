from random import seed

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import middleware
from app.auth.routes import auth
from app.database import get_db_session
from app.items.routes import items

seed()


def create_app():
    app = FastAPI(
        dependencies=[
            Depends(middleware.validate_jwt),
            Depends(get_db_session),
            Depends(middleware.check_authorization),
        ]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    app.include_router(auth)
    app.include_router(items)

    return app
