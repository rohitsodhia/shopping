import datetime

from pydantic import BaseModel


class NewReceiptInput(BaseModel):
    store_id: int
    date: datetime.date
    notes: str | None = None


class Receipt(BaseModel):
    id: int
    store_id: int
    date: datetime.date
    notes: str | None = None


class Item(BaseModel):
    id: int
    name: str


class Purchase(BaseModel):
    id: int
    item_id: int
    item: Item
    price: int | None = None
    notes: str | None = None


class ReceiptResponseData(BaseModel):
    receipt: Receipt


class ReceiptResponse(BaseModel):
    data: ReceiptResponseData


class ListPurchasesResponseData(BaseModel):
    purchases: list[Purchase]


class ListPurchasesResponse(BaseModel):
    data: ListPurchasesResponseData


class ListReceiptsResponseData(BaseModel):
    receipts: list[Receipt]
    page: int
    total: int


class ListReceiptsResponse(BaseModel):
    data: ListReceiptsResponseData


class UpdateReceiptInput(BaseModel):
    date: datetime.date
    notes: str | None = None
