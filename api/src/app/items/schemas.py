from pydantic import BaseModel


class NewItemInput(BaseModel):
    name: str


class Item(BaseModel):
    id: int
    name: str
    notes: str | None = None


class ItemResponseData(BaseModel):
    item: Item


class ItemResponse(BaseModel):
    data: ItemResponseData


class ListItemsResponseData(BaseModel):
    items: list[Item]
    page: int
    total: int


class ListItemsResponse(BaseModel):
    data: ListItemsResponseData


class GetItemResponse(BaseModel):
    data: ItemResponseData


class ItemInput(BaseModel):
    name: str | None = None
    notes: str | None = None
