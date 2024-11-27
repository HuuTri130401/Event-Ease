from datetime import datetime
from operator import and_
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db.database import get_db
from app.helpers.enum import UserRoleRequest
from app.models.model_user import User
from app.schemas.sche_user import UserRegisterRequest

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(and_(User.user_name == username, User.is_deleted == False)).first()
    
    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(and_(User.email == email, User.is_deleted == False)).first()

    def get_all_user(self):
        return self.session.query(User).filter(User.is_deleted == False)

    def get_user_by_id(self, id: int):
        return self.session.query(User).filter(and_(User.id == id, User.is_deleted == False)).first()

    def inactive_user(self, user_id: int):
        exist_user = self.session.query(User).filter(and_(User.id == user_id, User.is_deleted == False)).first()
        if exist_user:
            if exist_user.status == "inactive":
                exist_user.status = "active"
            elif exist_user.status == "active": 
                exist_user.status = "inactive"
            self.session.commit()

    def delete_user(self, user_id: int):
        exist_user = self.session.query(User).filter(and_(User.id == user_id, User.is_deleted == False)).first()
        if exist_user:
            exist_user.is_deleted = True
            self.session.commit()

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

def get_user_repository(session: Session = Depends(get_db)):
    return UserRepository(session)