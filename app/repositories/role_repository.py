from operator import and_
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.model_user import Role
from app.schemas.sche_role import RoleRequestCreate

class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_role(self):
        return self.session.query(Role).filter(Role.is_deleted == False) # Query thay List
    
    def get_role_by_id(self, id: int):
        return self.session.query(Role).filter(and_(Role.id == id, Role.is_deleted == False)).first()
    
    def get_role_by_name(self, name: str):
        return self.session.query(Role).filter(and_(Role.name == name, Role.is_deleted == False)).first()

    def get_list_role_by_ids(self, role_ids: list[int]):
        return self.session.query(Role).filter(and_(Role.id.in_(role_ids), Role.is_deleted == False)).all()

    def create_role(self, data: RoleRequestCreate):
        new_role = Role(
            name=data.name,
            description=data.description
        )
        self.session.add(new_role)
        self.session.commit()
        return new_role
    
def get_role_repository(session: Session = Depends(get_db)):
    return RoleRepository(session)