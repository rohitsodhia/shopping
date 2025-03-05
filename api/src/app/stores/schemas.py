from pydantic import BaseModel


class StoreInput(BaseModel):
    name: str


class Store(BaseModel):
    id: int
    name: str


class StoreResponseData(BaseModel):
    store: Store


class StoreResponse(BaseModel):
    data: StoreResponseData


class ListStoresResponseData(BaseModel):
    stores: list[Store]
    page: int


class ListStoresResponse(BaseModel):
    data: ListStoresResponseData
