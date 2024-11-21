from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return {"message": "User not found"}
        return user
    
    def get_all_user(self):
        users = self.user_repository.get_all_user()
        if not users:
            return {"message": "List user is empty"}
        return users