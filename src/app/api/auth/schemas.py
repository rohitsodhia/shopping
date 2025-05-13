from pydantic import BaseModel


class UserInput(BaseModel):
    password: str


class AuthResponse(BaseModel):
    jwt: str


class AuthFailedErrors(BaseModel):
    invalid: bool = True


class AuthFailed(BaseModel):
    errors: AuthFailedErrors
