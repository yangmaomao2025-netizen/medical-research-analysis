"""
API路由聚合
"""
from fastapi import APIRouter

from app.api.v1 import auth, literature, user, project, ai, research

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(literature.router)
api_router.include_router(user.router)
api_router.include_router(project.router)
api_router.include_router(ai.router)
api_router.include_router(research.router)
