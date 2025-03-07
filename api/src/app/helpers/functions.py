import re
from typing import Type

from pydantic import BaseModel


def dict_from_schema(obj, schema: Type[BaseModel]) -> dict:
    return schema.model_validate(obj, from_attributes=True).model_dump()


def parse_integrity_error(msg: str) -> tuple[str, int] | None:
    invalid_key = re.search(r"Key \((\w+?)\)=\((\w+?)\)", str(msg))
    if invalid_key:
        return invalid_key.group(1), int(invalid_key.group(2))
