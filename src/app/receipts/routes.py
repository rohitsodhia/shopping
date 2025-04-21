from datetime import date
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.configs import templates
from app.database import DBSessionDependency
from app.exceptions import AlreadyExists
from app.repositories import ReceiptRepository, StoreRepository

receipts = APIRouter(prefix="/receipts")


@receipts.get("", response_class=HTMLResponse)
async def list_receipts(
    request: Request, db_session: DBSessionDependency, page: int = 1
):
    store_repository = StoreRepository(db_session)
    stores = await store_repository.get_all()
    receipt_repository = ReceiptRepository(db_session)
    receipts = await receipt_repository.get_all(page=page)

    return templates.TemplateResponse(
        request=request,
        name="receipts.html",
        context={"stores": stores, "receipts": receipts},
    )


@receipts.post("", response_class=RedirectResponse)
async def process_new_receipt(
    request: Request,
    db_session: DBSessionDependency,
    date: Annotated[date, Form()],
    store_id: Annotated[int, Form()],
):
    receipt_repository = ReceiptRepository(db_session)
    await receipt_repository.create(store_id=store_id, date=date)

    return RedirectResponse(url="/receipts", status_code=302)


@receipts.get("/{receipt_id}/edit", response_class=HTMLResponse)
async def edit_receipt(
    request: Request,
    db_session: DBSessionDependency,
    receipt_id: int,
):
    receipt_repository = ReceiptRepository(db_session)
    receipt = await receipt_repository.get_by_id(receipt_id)
    store_repository = StoreRepository(db_session)
    stores = await store_repository.get_all()

    return templates.TemplateResponse(
        request=request,
        name="receipt_edit.html",
        context={"receipt": receipt, "stores": stores},
    )


@receipts.post("/{receipt_id}/edit", response_class=RedirectResponse)
async def process_edit_receipt(
    request: Request,
    db_session: DBSessionDependency,
    receipt_id: int,
    date: Annotated[date, Form()],
    notes: Annotated[str, Form()],
):
    receipt_repository = ReceiptRepository(db_session)
    await receipt_repository.update(id=receipt_id, date=date, notes=notes)

    return RedirectResponse(url="/receipts", status_code=302)


@receipts.get("/{receipt_id}", response_class=HTMLResponse)
async def view_receipt(
    request: Request,
    db_session: DBSessionDependency,
    receipt_id: int,
):
    receipt_repository = ReceiptRepository(db_session)
    receipt = await receipt_repository.get_by_id(receipt_id, with_store=True)

    return templates.TemplateResponse(
        request=request,
        name="receipt.html",
        context={"receipt": receipt},
    )
