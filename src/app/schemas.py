from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmptyData(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SuccessResponse(BaseModel):
    data: EmptyData


class AlreadyExistsResponseContent(BaseModel):
    error: Literal["already_exists"]
    msg: str


class AlreadyExistsResponse(BaseModel):
    errors: list[AlreadyExistsResponseContent] = Field(max_length=1)
