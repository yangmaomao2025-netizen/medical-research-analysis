"""
AI相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.services.auth import get_current_active_user
from app.services.ai import ai_service

router = APIRouter(prefix="/ai", tags=["AI服务"])

@router.post("/summarize")
async def summarize_literature(
    title: str,
    abstract: str,
    current_user: User = Depends(get_current_active_user)
):
    """AI总结文献"""
    try:
        result = await ai_service.summarize_paper(title, abstract)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate")
async def translate_text(
    text: str,
    target_lang: str = "zh",
    current_user: User = Depends(get_current_active_user)
):
    """AI翻译"""
    try:
        result = await ai_service.translate_text(text, target_lang)
        return {"translation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/research-topics")
async def suggest_research_topics(
    research_area: str,
    current_user: User = Depends(get_current_active_user)
):
    """智能选题建议"""
    try:
        result = await ai_service.suggest_research_topic(research_area)
        return {"topics": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
