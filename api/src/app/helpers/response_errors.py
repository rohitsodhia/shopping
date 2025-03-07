from fastapi.responses import JSONResponse


def error_response(status_code: int, content: list | None = None) -> JSONResponse:
    if content == None:
        content = []
    return JSONResponse(status_code=status_code, content={"errors": content})


def not_found_response():
    return error_response(status_code=404, content=[{"error": "not_found"}])


def fields_missing_response(fields: list[str]) -> JSONResponse:
    return error_response(
        status_code=400,
        content=[{"error": "missing_fields", "fields": fields}],
    )


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
