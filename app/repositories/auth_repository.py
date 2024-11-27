from operator import and_
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.model_user import User

class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def authentication_user(self, email: str):
        return self.session.query(User).filter(and_(User.email == email, User.is_deleted == False)).first()

def get_auth_repository(session: Session = Depends(get_db)):
    return AuthRepository(session)