import re
from typing import Type

from fastapi.responses import JSONResponse
from pydantic import BaseModel


def error_response(status_code: int, content: list | None = None) -> JSONResponse:
    if content == None:
        content = []
    return JSONResponse(status_code=status_code, content={"errors": content})


def integrity_error_response(msg: str) -> JSONResponse:
    return error_response(
        400,
        [
            {
                "error": "resource_not_found",
                "message": msg,
            }
        ],
    )


def dict_from_schema(obj, schema: Type[BaseModel]) -> dict:
    return schema.model_validate(obj, from_attributes=True).model_dump()


def parse_integrity_error(msg: str) -> tuple[str, int] | None:
    invalid_key = re.search(r"Key \((\w+?)\)=\((\w+?)\)", str(msg))
    if invalid_key:
        return invalid_key.group(1), int(invalid_key.group(2))
