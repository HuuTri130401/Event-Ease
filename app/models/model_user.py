from enum import unique
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table
from app.models.model_base import Base, BareBaseModel

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, primary_key=True),
    Column('role_id', Integer, primary_key=True)
)

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
    role = Column(String, default='Guest')
    company_id = Column(Integer, nullable=True)
    image_id = Column(Integer, nullable=True)

class Role(BareBaseModel):
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    