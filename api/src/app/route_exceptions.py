from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import AlreadyExists
from app.helpers.response_errors import error_response


def already_exists_exception_handler(
    request: Request, exc: AlreadyExists
) -> JSONResponse:
    return error_response(
        status_code=422, content=[{"error": "already_exists", "msg": str(exc)}]
    )
