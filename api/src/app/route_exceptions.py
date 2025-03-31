from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import AlreadyExists, NotFound
from app.helpers.responses import error_response


def already_exists_exception_handler(
    request: Request, exc: AlreadyExists
) -> JSONResponse:
    return error_response(
        status_code=422, content=[{"error": "already_exists", "msg": str(exc)}]
    )


def not_found_exception_handler(request: Request, exc: NotFound) -> JSONResponse:
    return error_response(status_code=404, content=[{"error": "not_found"}])
