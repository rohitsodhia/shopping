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


class ListItemsResponseData(BaseModel):
    items: list[Item]
    page: int


class ListItemsResponse(BaseModel):
    data: ListItemsResponseData


class GetItemResponseData(BaseModel):
    item: Item | None


class GetItemResponse(BaseModel):
    data: GetItemResponseData
