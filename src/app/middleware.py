import jwt
from fastapi import HTTPException, Request, status

from app.configs import configs


async def validate_jwt(request: Request):
    token = request.cookies.get("auth")
    request.scope["auth"] = None
    request.scope["user"] = None
    if token:
        try:
            jwt_body = jwt.decode(
                token,
                configs.JWT_SECRET_KEY,
                algorithms=[configs.JWT_ALGORITHM],
            )
            request.scope["user"] = "valid"
        except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
            pass
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )


async def check_authorization(request: Request):
    public = getattr(request.scope["route"].endpoint, "is_public", False)

    path = request.scope["route"].path
    if not public and request.scope["user"] == None:
        if not path.startswith("/api/"):
            raise HTTPException(
                status_code=302,
                detail="Not authorized",
                headers={"Location": "/login"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
