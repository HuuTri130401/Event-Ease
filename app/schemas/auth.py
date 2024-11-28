from typing import Optional
from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
