from enum import unique
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.models.model_base import BareBaseModel


class UserRole(BareBaseModel):
    user_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)


class User(BareBaseModel):
    full_name = Column(String, index=True)
    user_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    gender = Column(Boolean, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    status = Column(String, nullable=True)
    level = Column(String, nullable=True)
    role = Column(String, default="Guest")
    company_id = Column(Integer, nullable=True)
    image_id = Column(Integer, nullable=True)


class Role(BareBaseModel):
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
