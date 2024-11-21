from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.models.model_base import BareBaseModel

class User(BareBaseModel):
    full_name = Column(String, index=True)
    user_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    gender = Column(Boolean, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    status = Column(String, nullable=True)
    level = Column(String, nullable=True)
    role = Column(String, default='Guest')
    company_id = Column(Integer, nullable=True)
    image_id = Column(Integer, nullable=True)
