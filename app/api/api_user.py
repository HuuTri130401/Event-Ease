import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from app.helpers.exception_handler import CustomException
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.model_user import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse, UserRegisterRequest
from app.services.user_service import UserService, get_user_service

logger = logging.getLogger()
router = APIRouter()

@router.get("", response_model=Page[UserItemResponse], summary="Danh sách người dùng") #API Get list User
def get(params: PaginationParams = Depends()) -> Any:
    try:
        _query = db.session.query(User)
        users = paginate(model=User, query=_query, params=params)
        return users
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))

@router.get("/{id}", response_model=DataResponse[UserItemResponse], summary="Thông tin chi tiết người dùng")    
def get_detail(id: int, user_service: UserService = Depends(get_user_service)):
    try:
        data=user_service.get_user_by_id(id)
        return DataResponse().custom_response(code='200', message='Xem thông tin chi tiết người dùng', data=data)
    except CustomException as e:
        raise CustomException(http_code=400, code='400', message=str(e))

@router.post("", response_model=DataResponse[UserItemResponse], summary="Tạo mới người dùng")
def create_user(user_data: UserRegisterRequest, user_service: UserService = Depends(get_user_service)) -> Any:    
    try:
        new_user = user_service.create_user(user_data)
        return DataResponse().custom_response(code="201", message="Tạo mới người dùng thành công", data=new_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))