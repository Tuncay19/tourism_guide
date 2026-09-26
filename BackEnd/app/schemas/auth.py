from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    avatar_url: str | None = None
    role: str
    is_verified: bool
    interests: list[str] = []
    budget_level: str | None = None
    travel_style: str | None = None
    created_at: datetime


class TokenResponse(BaseModel):
    message: str
    token: str
    user: UserOut
