from fastapi.responses import JSONResponse


def error_response(status_code: int, content: list | None = None) -> JSONResponse:
    if content is None:
        content = []
    return JSONResponse(status_code=status_code, content={"errors": content})
