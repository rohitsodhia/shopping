import datetime

import bcrypt
import jwt
from fastapi import APIRouter

from app.auth import schemas
from app.configs import configs
from app.database import DBSessionDependency
from app.helpers.decorators import public
from app.helpers.response_errors import error_response

auth = APIRouter(prefix="/auth")


@auth.post(
    "/login",
    response_model=schemas.AuthResponse,
    responses={422: {"model": schemas.AuthFailed}},
)
@public
async def login(user_details: schemas.UserInput, db_session: DBSessionDependency):
    password = user_details.password
    password_check = bcrypt.checkpw(
        password.encode("utf-8"), configs.PASSWORD_HASH.encode("utf-8")
    )
    if password_check:
        # jwt = exp_len = {"weeks": 2}
        return {
            "jwt": jwt.encode(
                {
                    "exp": datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(weeks=2),
                },
                key=configs.JWT_SECRET_KEY,
                algorithm=configs.JWT_ALGORITHM,
            )
        }
    return error_response(status_code=422, content=[{"error": "invalid"}])
