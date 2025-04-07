from pydantic import BaseModel, ConfigDict


class StoreInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str


class Store(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: int
    name: str


class StoreResponseData(BaseModel):
    store: Store


class StoreResponse(BaseModel):
    data: StoreResponseData


class ListStoresResponseData(BaseModel):
    stores: list[Store]
    page: int
    total: int


class ListStoresResponse(BaseModel):
    data: ListStoresResponseData
