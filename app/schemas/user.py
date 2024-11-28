from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_deleted: Optional[bool] = None


class UserItemResponse(UserBase):
    id: int
    full_name: str
    email: EmailStr
    user_name: str
    gender: bool
    date_of_birth: datetime
    phone: str
    address: str
    status: Optional[str] = None
    level: Optional[str] = None
    company_id: Optional[int] = None
    image_id: Optional[int] = None


class UserRegisterRequest(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    full_name: Optional[str]
    gender: Optional[bool]
    date_of_birth: Optional[datetime]
    phone: Optional[str]
    address: Optional[str]


class UserRequestUpdate(BaseModel):
    user_name: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[bool] = None
    date_of_birth: Optional[datetime] = None
    phone: Optional[str] = None
    address: Optional[str] = None
