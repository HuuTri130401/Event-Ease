from typing import Optional
from pydantic import BaseModel
from app.schemas.base import SchemaBase


class RoleRequestCreate(BaseModel):
    name: str
    description: str


class RoleRequestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(SchemaBase):
    id: int
    name: str
    description: str
