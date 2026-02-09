"""
用户管理服务
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from app.db.models import User
from app.models.user import UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def update_profile(
        self,
        user_id: uuid.UUID,
        data: UserUpdate
    ) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_academic_profile(self, user_id: uuid.UUID) -> dict:
        """获取学术画像"""
        # TODO: 从成果表统计数据
        return {
            "h_index": 0,
            "total_citations": 0,
            "total_papers": 0,
            "total_impact_factor": 0.0,
            "paper_trend": [],
            "research_areas": []
        }
