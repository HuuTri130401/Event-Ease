
from datetime import datetime
from fastapi import Depends, logger
from fastapi_sqlalchemy import db
from pydantic import Field
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db.database import get_db
from app.helpers.enum import UserRoleRequest
from app.models.model_user import User, user_roles
from app.schemas.sche_user import UserRegisterRequest

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.user_name == username).first()
    
    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_all_user(self):
        return self.session.query(User).filter(User.is_deleted == 0, User.status != "inactive").all()

    def get_user_by_id(self, id: int):
        return self.session.query(User).filter(User.id == id).first()

    def create_user(self, data: UserRegisterRequest):
        print(f"Received data in repo: {data}")
        new_user = User(
            full_name = data.full_name,
            user_name = data.user_name,
            email = data.email,
            hashed_password = get_password_hash(data.password),
            gender = data.gender,
            date_of_birth = data.date_of_birth,
            phone = data.phone,
            address = data.address,
            created_at = datetime.now(),
            role = UserRoleRequest.GUEST.value,
            is_deleted = False,
            status = 'active'
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def assign_role_to_user(self, user_id: int, role_id: int):
        user_role = user_roles(user_id, role_id)
        self.session.add(user_role)
        self.session.commit()

    def remove_role_from_user(self, user_id: int, role_id: int):
        user_role = self.session.query(user_roles).filter_by(user_id=user_id, role_id=role_id).first()
        if user_role:
            self.session.delete(user_role)
            self.session.commit()

def get_user_repository(session: Session = Depends(get_db)):
    return UserRepository(session)