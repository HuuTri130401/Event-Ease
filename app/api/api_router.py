# Tổ chức và định tuyến API Endpoint FastAPI
from fastapi import APIRouter  # Group Endpoint
from app.api import api_auth, api_user, api_role

router = APIRouter()
router.include_router(api_user.router, tags=["User"], prefix="/api/user")
router.include_router(api_role.router, tags=["Role"], prefix="/api/role")
router.include_router(api_auth.router, tags=["Auth"], prefix="/api/auth")
