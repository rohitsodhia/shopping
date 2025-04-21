from pydantic import BaseModel


class NewPurchaseInput(BaseModel):
    item_id: int
    receipt_id: int
    price: int | None = None
    notes: str | None = None


class Purchase(BaseModel):
    id: int
    item_id: int
    receipt_id: int
    price: int | None = None
    notes: str | None = None


class PurchaseResponseData(BaseModel):
    purchase: Purchase


class NewPurchaseResponse(BaseModel):
    data: PurchaseResponseData


class NewPurchaseBulkPurchaseInput(BaseModel):
    item_id: int
    price: int | None = None
    notes: str | None = None


class NewPurchaseBulkInput(BaseModel):
    receipt_id: int
    purchases: list[NewPurchaseBulkPurchaseInput]


class NewPurchaseBulkData(BaseModel):
    purchases: list[Purchase]


class NewPurchaseBulkResponse(BaseModel):
    data: NewPurchaseBulkData


class UpdatePurchaseInput(BaseModel):
    price: int | None = None
    notes: str | None = None


class UpdatePurchaseResponse(BaseModel):
    data: PurchaseResponseData
