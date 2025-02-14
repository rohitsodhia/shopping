import datetime

import bcrypt
import jwt
from envs import JWT_ALGORITHM, JWT_SECRET_KEY
from fastapi import APIRouter, status

from app.auth import schemas
from app.database import DBSessionDependency
from app.envs import PASSWORD_HASH
from app.helpers.decorators import public
from app.helpers.functions import error_response
from app.schemas import ErrorResponse

auth = APIRouter(prefix="/auth")


@auth.post(
    "/login",
    response_model=schemas.AuthResponse,
    responses={404: {"model": ErrorResponse(error=schemas.AuthFailed())}},
)
@public
async def login(user_details: schemas.UserInput, db_session: DBSessionDependency):
    password = user_details.password
    password_check = bcrypt.checkpw(
        password.encode("utf-8"), PASSWORD_HASH.encode("utf-8")
    )
    if password_check:
        # jwt = exp_len = {"weeks": 2}
        return {
            "jwt": jwt.encode(
                {
                    "exp": datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(weeks=2),
                },
                key=JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM,
            )
        }
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"invalid": True},
    )
