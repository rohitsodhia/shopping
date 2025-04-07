from typing import Literal

from pydantic import BaseModel, Field


class AlreadyExistsResponseContent(BaseModel):
    error: Literal["already_exists"]
    msg: str


class AlreadyExistsResponse(BaseModel):
    errors: list[AlreadyExistsResponseContent] = Field(max_length=1)
