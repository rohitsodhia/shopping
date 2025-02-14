from pydantic import BaseModel


class UserInput(BaseModel):
    password: str


class AuthResponse(BaseModel):
    jwt: str


class AuthFailed(BaseModel):
    invalid: bool = True
