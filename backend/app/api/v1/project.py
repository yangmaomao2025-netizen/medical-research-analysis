"""
项目路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.db.database import get_db
from app.db.models import User
from app.models.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, 
    ProjectStatus
)
from app.services.project import ProjectService
from app.services.auth import get_current_active_user

router = APIRouter(prefix="/projects", tags=["项目"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建项目"""
    service = ProjectService(db)
    project = service.create(data, current_user.id)
    return project

@router.get("", response_model=List[ProjectResponse])
async def get_my_projects(
    status: Optional[ProjectStatus] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取我的项目列表"""
    service = ProjectService(db)
    items, total = service.get_user_projects(current_user.id, status, skip, limit)
    return items

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取项目详情"""
    service = ProjectService(db)
    project = service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新项目"""
    service = ProjectService(db)
    project = service.update(project_id, data, current_user.id)
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除项目"""
    service = ProjectService(db)
    service.delete(project_id, current_user.id)
    return {"message": "Project deleted successfully"}
