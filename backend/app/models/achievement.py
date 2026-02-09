"""
成果模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class AchievementType(str, Enum):
    PAPER = "paper"
    PATENT = "patent"
    SOFTWARE_COPYRIGHT = "software_copyright"
    CONFERENCE = "conference"
    FUNDING = "funding"
    BOOK = "book"
    AWARD = "award"

class PaperStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REVISION = "revision"
    ACCEPTED = "accepted"
    PUBLISHED = "published"
    REJECTED = "rejected"

class AchievementBase(BaseModel):
    achievement_type: AchievementType
    title: str
    authors: Optional[List[str]] = []
    publish_date: Optional[datetime] = None
    journal: Optional[str] = None
    impact_factor: Optional[float] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None

# 论文专用
class PaperCreate(AchievementBase):
    achievement_type: AchievementType = AchievementType.PAPER
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = []
    status: PaperStatus = PaperStatus.DRAFT
    citation_count: Optional[int] = 0

# 基金专用  
class FundingCreate(AchievementBase):
    achievement_type: AchievementType = AchievementType.FUNDING
    funding_type: Optional[str] = None  # 国自然、省自然等
    amount: Optional[float] = None
    project_number: Optional[str] = None
    duration: Optional[str] = None

class AchievementResponse(AchievementBase):
    id: UUID
    created_by: UUID
    project_id: Optional[UUID] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AcademicProfile(BaseModel):
    """学术画像"""
    h_index: Optional[int] = 0
    total_citations: Optional[int] = 0
    total_papers: Optional[int] = 0
    total_impact_factor: Optional[float] = 0.0
    funding_total: Optional[float] = 0.0
    paper_trend: Optional[List[dict]] = []  # 发文趋势
    research_areas: Optional[List[dict]] = []  # 研究领域分布
