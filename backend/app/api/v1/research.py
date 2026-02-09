"""
科研辅助API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.services.auth import get_current_active_user
from app.services.research import research_service

router = APIRouter(prefix="/research", tags=["科研辅助"])

@router.post("/protocol/generate")
async def generate_protocol(
    title: str,
    study_type: str,
    disease: str,
    objectives: str,
    current_user: User = Depends(get_current_active_user)
):
    """生成研究方案"""
    try:
        result = await research_service.generate_protocol(
            title, study_type, disease, objectives
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiment/design")
async def design_experiment(
    research_question: str,
    available_resources: list,
    current_user: User = Depends(get_current_active_user)
):
    """设计实验"""
    try:
        result = await research_service.design_experiment(
            research_question, available_resources
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/statistics/plan")
async def statistical_plan(
    data_type: str,
    groups: int,
    primary_endpoint: str,
    current_user: User = Depends(get_current_active_user)
):
    """统计分析方案"""
    try:
        result = await research_service.statistical_analysis_plan(
            data_type, groups, primary_endpoint
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
