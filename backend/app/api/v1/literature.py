"""
文献路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.db.database import get_db
from app.db.models import User
from app.models.literature import (
    LiteratureCreate, LiteratureUpdate, LiteratureResponse, 
    LiteratureList, LiteratureSearch
)
from app.services.literature import LiteratureService
from app.services.auth import get_current_active_user

router = APIRouter(prefix="/literatures", tags=["文献"])

@router.post("", response_model=LiteratureResponse, status_code=status.HTTP_201_CREATED)
async def create_literature(
    data: LiteratureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建文献"""
    service = LiteratureService(db)
    literature = service.create(data, current_user.id)
    return literature

@router.get("/search", response_model=LiteratureList)
async def search_literatures(
    keyword: Optional[str] = None,
    diseases: Optional[List[str]] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    is_sci: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """搜索文献"""
    service = LiteratureService(db)
    search_params = LiteratureSearch(
        keyword=keyword,
        diseases=diseases,
        year_from=year_from,
        year_to=year_to,
        is_sci=is_sci,
        page=page,
        page_size=page_size
    )
    items, total = service.search(search_params, current_user.id)
    return {"total": total, "items": items}

@router.get("/{literature_id}", response_model=LiteratureResponse)
async def get_literature(
    literature_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取文献详情"""
    service = LiteratureService(db)
    literature = service.get_by_id(literature_id)
    if not literature:
        raise HTTPException(status_code=404, detail="Literature not found")
    return literature

@router.put("/{literature_id}", response_model=LiteratureResponse)
async def update_literature(
    literature_id: uuid.UUID,
    data: LiteratureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新文献"""
    service = LiteratureService(db)
    literature = service.update(literature_id, data, current_user.id)
    return literature

@router.delete("/{literature_id}")
async def delete_literature(
    literature_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除文献"""
    service = LiteratureService(db)
    service.delete(literature_id, current_user.id)
    return {"message": "Literature deleted successfully"}

@router.post("/{literature_id}/upload")
async def upload_literature_file(
    literature_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """上传文献PDF"""
    # TODO: 实现文件上传到MinIO
    return {"message": "File upload endpoint", "filename": file.filename}
