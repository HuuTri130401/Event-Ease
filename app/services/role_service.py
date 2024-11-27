from fastapi import Depends, HTTPException
from app.helpers.exception_handler import CustomException
from app.repositories.role_repository import RoleRepository, get_role_repository
from app.schemas.sche_role import RoleRequestCreate, RoleRequestUpdate


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
    
    def get_all_role(self):
        roles = self.role_repository.get_all_role()
        if not roles:
            raise HTTPException(status_code=400, detail="Danh sách role đang trống!")
        return roles
    
    def get_role_by_id(self, id: int):
        role = self.role_repository.get_role_by_id(id)
        if not role: 
            raise HTTPException(status_code=404, detail=f"Không tìm thấy role có id là: {id}!")
        return role

    def create_role(self, data: RoleRequestCreate):
        exist_role = self.role_repository.get_role_by_name(data.name)
        if not exist_role:
            new_role = self.role_repository.create_role(data)
            return new_role
        raise HTTPException(status_code=400, detail=f"Role có tên {data.name} đã tồn tại!")
    
    def update_role(self, data: RoleRequestUpdate, id: int):
        exist_role = self.role_repository.get_role_by_id(id)
        if not exist_role:
            raise HTTPException(status_code=400, detail=f'Role không tồn tại!!')
        self.role_repository.update_role(data, id)

    def delete_role(self, role_id: int):
        exist_role = self.role_repository.get_role_by_id(role_id)
        if not exist_role:
            raise HTTPException(status_code=400, detail=f'Role không tồn tại!!')
        self.role_repository.delete_role(role_id)

def get_role_service(role_repository: RoleRepository = Depends(get_role_repository)):
       return RoleService(role_repository)