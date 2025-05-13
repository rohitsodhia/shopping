from pydantic import BaseModel, ConfigDict


class NewItemInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str


class Item(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

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
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = None
    notes: str | None = None
