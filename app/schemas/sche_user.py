from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# CHƯA UPDATE CHUẨN FIELD
class UserBase(BaseModel): 
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True

class UserItemResponse(UserBase):
    id: int
    full_name: str
    email: EmailStr
    user_name: str
    gender: bool
    date_of_birth: datetime
    phone: str
    address: str
    status: str
    level: str
    role: str
    company_id: int
    image_id: int