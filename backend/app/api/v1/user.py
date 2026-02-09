"""
用户路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.models.user import UserResponse, UserUpdate
from app.services.auth import get_current_active_user
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["用户"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    """获取我的个人信息"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新我的个人信息"""
    service = UserService(db)
    user = service.update_profile(current_user.id, data)
    return user

@router.get("/me/academic-profile")
async def get_my_academic_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取我的学术画像"""
    service = UserService(db)
    profile = service.get_academic_profile(current_user.id)
    return profile
