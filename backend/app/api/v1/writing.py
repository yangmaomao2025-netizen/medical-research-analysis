"""
论文写作API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import User
from app.services.auth import get_current_active_user
from app.services.writing import writing_service

router = APIRouter(prefix="/writing", tags=["论文写作"])

@router.post("/outline/generate")
async def generate_outline(
    title: str,
    paper_type: str,
    sections: List[str],
    current_user: User = Depends(get_current_active_user)
):
    """生成论文大纲"""
    try:
        result = await writing_service.generate_outline(title, paper_type, sections)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/polish")
async def polish_text(
    text: str,
    polish_type: str = "academic",
    target_journal: str = None,
    current_user: User = Depends(get_current_active_user)
):
    """润色文本"""
    try:
        result = await writing_service.polish_text(text, polish_type, target_journal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/references/suggest")
async def suggest_references(
    topic: str,
    keywords: List[str],
    num_suggestions: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """推荐参考文献"""
    try:
        result = await writing_service.suggest_references(topic, keywords, num_suggestions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
