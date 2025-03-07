from fastapi.responses import JSONResponse


def error_response(status_code: int, content: list | None = None) -> JSONResponse:
    if content == None:
        content = []
    return JSONResponse(status_code=status_code, content={"errors": content})


def already_exists_error(obj: dict) -> dict:
    return {
        "error": "already_exists",
        "object": obj,
    }


def integrity_error_response(msg: str) -> dict:
    return {
        "error": "resource_not_found",
        "message": msg,
    }
