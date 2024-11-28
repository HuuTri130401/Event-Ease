import logging
import traceback
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.exception_handler import CustomException
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.model_user import Role
from app.schemas.base import DataResponse
from app.schemas.role import RoleResponse, RoleRequestCreate, RoleRequestUpdate
from app.services.role_service import RoleService, get_role_service

logger = logging.getLogger()
router = APIRouter()


@router.get("", response_model=Page[RoleResponse], summary="Danh sách roles")
def get(
    params: PaginationParams = Depends(),
    role_service: RoleService = Depends(get_role_service),
) -> Any:
    try:
        _query = role_service.get_all_role()
        roles = paginate(model=Role, query=_query, params=params)
        return roles
    except Exception as e:
        error_details = traceback.format_exc()  # Lấy traceback đầy đủ
        print(f"Error occurred: {error_details}")
        raise CustomException(
            http_code=400, code="400", message=f"{str(e)}: {error_details}"
        )


@router.get(
    "/{id}", response_model=DataResponse[RoleResponse], summary="Xem chi tiết role"
)
def get_detail(id: int, role_service: RoleService = Depends(get_role_service)) -> Any:
    try:
        role = role_service.get_role_by_id(id)
        return DataResponse().custom_response(
            code="200", message="Thông tin chi tiết", data=role
        )
    except Exception as e:
        raise CustomException(http_code=404, code="404", message=str(e))


@router.post("", response_model=DataResponse[RoleResponse], summary="Tạo mới role")
def create_role(
    role_data: RoleRequestCreate, role_service: RoleService = Depends(get_role_service)
) -> Any:
    try:
        new_role = role_service.create_role(role_data)
        return DataResponse().custom_response(
            code="201", message="Tạo mới role thành công", data=new_role
        )
    except Exception as e:
        raise CustomException(http_code=400, code="400", message=str(e))


@router.put("/{id}", response_model=DataResponse[RoleResponse], summary="Cập nhật role")
def update_role(
    id: int,
    role_data: RoleRequestUpdate,
    role_service: RoleService = Depends(get_role_service),
) -> Any:
    try:
        role = role_service.update_role(role_data, id)
        return DataResponse().custom_response(
            code="200", message="Cập nhật role thành công", data=role
        )
    except Exception as e:
        raise CustomException(http_code=400, code="400", message=str(e))


@router.delete("/delete_role/{id}", summary="Xóa role")
def delete_user(id: int, role_service: RoleService = Depends(get_role_service)):
    try:
        result = role_service.delete_role(role_id=id)
        return DataResponse().custom_response(
            code="200", message=f"Xóa role thành công", data=result
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error occurred: {error_details}")
        raise CustomException(http_code=400, code="400", message=str(e))
