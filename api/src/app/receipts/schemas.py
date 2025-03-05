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


class ReceiptResponseData(BaseModel):
    receipt: Receipt


class ReceiptResponse(BaseModel):
    data: ReceiptResponseData
