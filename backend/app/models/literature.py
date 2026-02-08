"""
文献相关模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class LiteratureType(str, Enum):
    JOURNAL = "journal"
    THESIS = "thesis"
    CONFERENCE = "conference"
    BOOK = "book"
    PATENT = "patent"
    OTHER = "other"

class LiteratureBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = []
    diseases: Optional[List[str]] = []
    authors: Optional[List[str]] = []
    author_units: Optional[List[str]] = []
    first_author: Optional[str] = None
    corresponding_author: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    literature_type: Optional[LiteratureType] = None
    study_types: Optional[List[str]] = []
    source: Optional[str] = None
    is_sci: Optional[bool] = False
    level: Optional[str] = None
    cas_partition: Optional[str] = None
    jcr_partition: Optional[str] = None
    impact_factor: Optional[float] = None
    text_availability: Optional[str] = "abstract"

class LiteratureCreate(LiteratureBase):
    pass

class LiteratureUpdate(BaseModel):
    title: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    diseases: Optional[List[str]] = None
    literature_type: Optional[LiteratureType] = None
    study_types: Optional[List[str]] = None

class LiteratureResponse(LiteratureBase):
    id: UUID
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    status: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LiteratureList(BaseModel):
    total: int
    items: List[LiteratureResponse]

class LiteratureSearch(BaseModel):
    keyword: Optional[str] = None
    diseases: Optional[List[str]] = None
    literature_types: Optional[List[LiteratureType]] = None
    study_types: Optional[List[str]] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    is_sci: Optional[bool] = None
    page: int = 1
    page_size: int = 20
