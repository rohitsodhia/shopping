from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import AlreadyExists, NotFound
from app.helpers.responses import error_response


def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_403_FORBIDDEN:
        response = error_response(
            status_code=status.HTTP_403_FORBIDDEN, content=[{"error": "forbidden"}]
        )
        response.delete_cookie(key="auth")
        return response
    else:
        return error_response(
            status_code=exc.status_code, content=[{"error": str(exc.detail)}]
        )


def already_exists_exception_handler(
    request: Request, exc: AlreadyExists
) -> JSONResponse:
    return error_response(
        status_code=422, content=[{"error": "already_exists", "msg": str(exc)}]
    )


def not_found_exception_handler(request: Request, exc: NotFound) -> JSONResponse:
    return error_response(status_code=404, content=[{"error": "not_found"}])
