"""
项目模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING = "pending"  # 申请中
    APPROVED = "approved"  # 已立项
    RECRUITING = "recruiting"  # 招募中
    IN_PROGRESS = "in_progress"  # 进行中
    FOLLOW_UP = "follow_up"  # 随访中
    COMPLETED = "completed"  # 已结题
    SUSPENDED = "suspended"  # 暂停

class ProjectType(str, Enum):
    CLINICAL_TRIAL = "clinical_trial"  # 临床试验
    RETROSPECTIVE = "retrospective"  # 回顾性研究
    BASIC_RESEARCH = "basic_research"  # 基础研究
    REAL_WORLD = "real_world"  # 真实世界研究
    OTHER = "other"

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_type: ProjectType
    status: ProjectStatus = ProjectStatus.PENDING
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    funding_source: Optional[str] = None  # 经费来源
    keywords: Optional[List[str]] = []
    diseases: Optional[List[str]] = []

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None

class ProjectMember(BaseModel):
    user_id: UUID
    role: str  # PI, Co-PI, Member, Data Entry, Statistician
    contribution_rate: Optional[int] = None  # 贡献百分比

class ProjectResponse(ProjectBase):
    id: UUID
    created_by: UUID
    members: Optional[List[ProjectMember]] = []
    progress_percent: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
