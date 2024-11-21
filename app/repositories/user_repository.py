
from sqlalchemy.orm import Session
from app.models.model_user import User

class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.user_name == username).first()
    
    def get_all_user(sefl):
        return sefl.db.query(User).all()