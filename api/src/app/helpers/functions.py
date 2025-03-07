from typing import Type

from fastapi.responses import JSONResponse
from pydantic import BaseModel


def error_response(status_code: int, content: list | None = None) -> JSONResponse:
    if content == None:
        content = []
    return JSONResponse(status_code=status_code, content={"errors": content})


def dict_from_schema(obj, schema: Type[BaseModel]) -> dict:
    return schema.model_validate(obj, from_attributes=True).model_dump()
