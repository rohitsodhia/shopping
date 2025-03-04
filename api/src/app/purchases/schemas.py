from pydantic import BaseModel

from app.models import store


class NewPurchaseInput(BaseModel):
    item_id: int
    price: float
    store_id: int | None = None
    store_name: str | None = None
    notes: str | None = None


class Store(BaseModel):
    id: int
    name: str


class Purchase(BaseModel):
    id: int
    item_id: int
    price: float
    store: Store
    notes: str | None = None


class NewPurchaseResponseData(BaseModel):
    purchase: Purchase


class NewPurchaseResponse(BaseModel):
    data: NewPurchaseResponseData

