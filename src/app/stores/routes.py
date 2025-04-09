from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.configs import templates

stores = APIRouter(prefix="/stores")


@stores.get("", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="stores.html", context={})
