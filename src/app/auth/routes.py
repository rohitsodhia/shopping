from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.configs import templates
from app.helpers.decorators import public

auth = APIRouter(prefix="/login")


@auth.get("", response_class=HTMLResponse)
@public
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})
