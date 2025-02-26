from pydantic import BaseModel


class NewItemInput(BaseModel):
    name: str


class Item(BaseModel):
    id: int
    name: str


class NewItemResponseData(BaseModel):
    item: Item


class NewItemResponse(BaseModel):
    data: NewItemResponseData

