import jwt
from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.configs import configs


async def validate_jwt(request: Request):
    token = request.headers.get("Authorization")
    request.scope["auth"] = None
    request.scope["user"] = None
    if token and token[:7] == "Bearer ":
        token = token[7:]
        try:
            jwt_body = jwt.decode(
                token,
                configs.JWT_SECRET_KEY,
                algorithms=[configs.JWT_ALGORITHM],
            )
            request.scope["user"] = "valid"
        except:
            pass


async def check_authorization(request: Request):
    public = getattr(request.scope["route"].endpoint, "is_public", False)

    path = request.scope["route"].path
    if not public and not path.startswith("/api/"):
        raise HTTPException(
            status_code=302,
            detail="Not authorized",
            headers={"Location": "/login"},
        )
    elif not public and request.scope["user"] == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
