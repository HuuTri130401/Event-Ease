import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.sche_auth import LoginRequest, TokenResponse
from app.schemas.sche_base import DataResponse
from app.services.auth_service import AuthService, get_auth_service

logger = logging.getLogger()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=DataResponse[TokenResponse], summary="Đăng nhập")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> Any:
#     try:
#         access_token = auth_service.authentication_user(form_data.username, form_data.password)
#         return DataResponse().custom_response(code = '200', message="Đăng nhập thành công", data=access_token)
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Thông tin xác thực không hợp lệ")
    
def login_for_access_token(request: LoginRequest = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> Any:
    try:
        access_token = auth_service.authentication_user(request)
        print(f"****************{access_token}")
        return DataResponse().custom_response(code = '200', message="Đăng nhập thành công", data=access_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Thông tin xác thực không hợp lệ")   