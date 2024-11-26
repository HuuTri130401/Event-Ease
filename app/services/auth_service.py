from fastapi import Depends, HTTPException
from pydantic import EmailStr
from app.core.security import create_access_token, verify_password
from app.repositories.auth_repository import AuthRepository, get_auth_repository
from app.schemas.sche_auth import LoginRequest, TokenResponse


class AuthService:
    def __init__(self, auth_repository: AuthRepository): 
        self.auth_repository = auth_repository

    def authentication_user(self, request: LoginRequest):
        user = self.auth_repository.authentication_user(request.email)
        if not user:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy người dùng có email là: {request.email}!")
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=400, detail=f"Thông tin đăng nhập không hợp lệ!")
        access_token = create_access_token(data={"sub": user.user_name})
        token_response = TokenResponse(
            access_token=access_token
        )
        return token_response
    
def get_auth_service(auth_repositoty: AuthRepository = Depends(get_auth_repository)):
    return AuthService(auth_repositoty)