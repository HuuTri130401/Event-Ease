import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_current_user
from app.models.model_user import User
from app.schemas.sche_auth import LoginRequest, TokenResponse
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse
from app.services.auth_service import AuthService, get_auth_service

logger = logging.getLogger()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=DataResponse[TokenResponse], summary="Đăng nhập") 
def login_for_access_token(request: LoginRequest = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> Any:
    try:
        access_token = auth_service.authentication_user(request)
        return DataResponse().custom_response(code = '200', message="Đăng nhập thành công", data=access_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Thông tin xác thực không hợp lệ")   
    
@router.get("/me", response_model=DataResponse[UserItemResponse], summary="About me")
def read_me(current_user: User = Depends(get_current_user)):
    return DataResponse().custom_response(code = '200', message="Thông tin profile", data=current_user)