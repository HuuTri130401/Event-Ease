
from pydantic import BaseModel
from app.schemas.sche_base import SchemaBase

class RoleRequestCreate(BaseModel):
    name: str
    description: str

class RoleReponse(SchemaBase):
    id: int
    name: str
    description: str
