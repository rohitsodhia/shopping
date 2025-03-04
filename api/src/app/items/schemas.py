from pydantic import BaseModel


class NewItemInput(BaseModel):
    name: str


class Item(BaseModel):
    id: int
    name: str
    notes: str | None = None


class NewItemResponseData(BaseModel):
    item: Item


class NewItemResponse(BaseModel):
    data: NewItemResponseData


class ListItemsResponseData(BaseModel):
    items: list[Item]
    page: int


class ListItemsResponse(BaseModel):
    data: ListItemsResponseData


class GetItemResponseData(BaseModel):
    item: Item | None


class GetItemResponse(BaseModel):
    data: GetItemResponseData


class ItemInput(BaseModel):
    name: str | None = None
    notes: str | None = None


class UpdateItemResponseData(BaseModel):
    item: Item


class UpdateItemResponse(BaseModel):
    data: GetItemResponseData
