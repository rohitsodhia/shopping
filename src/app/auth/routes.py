from typing import Annotated

import bcrypt
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.auth import functions
from app.configs import configs, templates
from app.helpers.decorators import public

auth = APIRouter(prefix="/login")


@auth.get("", response_class=HTMLResponse)
@public
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@auth.post("", response_class=RedirectResponse)
@public
async def process_login(request: Request, password: Annotated[str, Form()]):
    password_check = bcrypt.checkpw(
        password.encode("utf-8"), configs.PASSWORD_HASH.encode("utf-8")
    )
    if not password_check:
        return RedirectResponse(url="/login?incorrect=1", status_code=302)

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="auth", value=functions.generate_token(), httponly=True)
    return response
