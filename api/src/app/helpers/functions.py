from fastapi.responses import JSONResponse


def error_response(status_code: int, content: dict | None = None) -> JSONResponse:
    if content == None:
        content = {}
    return JSONResponse(status_code=status_code, content={"errors": content})
