import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.model_user import User
from app.schemas.sche_user import UserItemResponse

logger = logging.getLogger()
router = APIRouter()

# @router.get("", dependencies=[Depends(login_required)], response_model=Page[UserItemResponse])
@router.get("", response_model=Page[UserItemResponse]) #API Get list User
def get(params: PaginationParams = Depends()) -> Any:
    try:
        _query = db.session.query(User)
        users = paginate(model=User, query=_query, params=params)
        return users
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))