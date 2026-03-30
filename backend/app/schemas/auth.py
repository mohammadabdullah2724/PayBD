from datetime import timedelta
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {"extra": "forbid"}


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str

    model_config = {"extra": "forbid"}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    model_config = {"extra": "forbid"}


class UserRead(BaseModel):
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {"extra": "forbid"}
