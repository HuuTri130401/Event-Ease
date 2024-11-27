from fastapi import Depends, HTTPException
from app.repositories.role_repository import RoleRepository, get_role_repository
from app.repositories.user_repository import UserRepository, get_user_repository
from app.repositories.user_role_repository import UserRoleRepository, get_user_role_repository
from app.schemas.sche_user import UserRegisterRequest
from app.models.model_user import user_roles
from app.schemas.sche_user_role import UserWithRolesResponse

class UserService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository, user_role_repository: UserRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail=f"Người dùng không không tồn tại")
        if user.is_deleted == True or user.status == "inactive":
            raise HTTPException(status_code=404, detail=f"Người dùng: {user.email} không hợp lệ")
        return user
    
    def get_user_by_id(self, id: int):
        user = self.user_repository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Người dùng không không tồn tại")
        if user.is_deleted == True or user.status == "inactive":
            raise HTTPException(status_code=404, detail=f"Người dùng: {user.email} không hợp lệ")
        return user

    def get_roles_by_user_id(self, user_id: int):
        print(f"user id: {user_id}")
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng này không có vai trò nào!")
        
        print(f"user: {user}")

        roles = self.user_role_repository.get_roles_by_user_id(user_id)
        print(f"roles: {roles}")

        return UserWithRolesResponse(
            user_id=user.id,
            full_name=user.full_name,
            user_name=user.user_name,
            email=user.email,
            phone=user.phone,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            status=user.status,
            level=user.level,
            roles=roles  # Ánh xạ vai trò
        )

    def get_all_user(self):
        users = self.user_repository.get_all_user()
        if not users:
            raise HTTPException(status_code=400, detail="Danh sách role đang trống!")
        return users
    
    def create_user(self, data: UserRegisterRequest):
        exist_user = self.user_repository.get_user_by_email(data.email)
        if not exist_user:
            new_user = self.user_repository.create_user(data)
            return new_user
        raise HTTPException(status_code=400, detail=f'Email {data.email} đã tồn tại!')

    def assign_roles_to_user(self, user_id: int, role_ids: list[int]):
        exist_user = self.user_repository.get_user_by_id(user_id)
        if not exist_user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại!")

        exist_roles = self.user_role_repository.get_roles_by_user_id(user_id)
        existing_role_ids = {role.id for role in exist_roles} # Lấy role id trong exist_roles
        role_id_not_assign_yet = [role_id for role_id in role_ids if role_id not in existing_role_ids]
        valid_roles = self.role_repository.get_list_role_by_ids(role_id_not_assign_yet)
        if not valid_roles:
            raise HTTPException(status_code=404, detail="Không tìm thấy vai trò nào hợp lệ")

        for role_id in role_id_not_assign_yet:
            self.user_role_repository.assign_role_to_user(user_id=user_id, role_id=role_id)

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        role_repository: RoleRepository = Depends(get_role_repository),
        user_role_repository: UserRoleRepository = Depends(get_user_role_repository)
    ):
    return UserService(
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository
        )