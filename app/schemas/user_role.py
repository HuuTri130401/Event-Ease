from datetime import datetime
from typing import List, Optional
from app.schemas.base import SchemaBase


class RoleResponse(SchemaBase):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class UserWithRolesResponse(SchemaBase):
    user_id: int
    full_name: str
    user_name: str
    email: str
    phone: str
    gender: bool
    date_of_birth: datetime
    status: Optional[str] = None
    level: Optional[str] = None
    roles: List[RoleResponse]  # Danh sách các vai trò của user

    class Config:
        from_attributes = True
