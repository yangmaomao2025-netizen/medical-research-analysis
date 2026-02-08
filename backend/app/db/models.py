"""
数据库模型定义
"""
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Text, 
    ForeignKey, JSON, Enum, Numeric, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
import uuid

class Base(DeclarativeBase):
    pass

# 枚举定义
class UserRole(str, PyEnum):
    SUPER_ADMIN = "super_admin"
    HOSPITAL_ADMIN = "hospital_admin"
    DEPT_ADMIN = "dept_admin"
    DOCTOR = "doctor"
    RESEARCHER = "researcher"
    STUDENT = "student"

class LiteratureType(str, PyEnum):
    JOURNAL = "journal"
    THESIS = "thesis"
    CONFERENCE = "conference"
    BOOK = "book"
    NEWSPAPER = "newspaper"
    REPORT = "report"
    PATENT = "patent"
    STANDARD = "standard"
    YEARBOOK = "yearbook"
    LAW = "law"
    OTHER = "other"

class StudyType(str, PyEnum):
    META_ANALYSIS = "meta_analysis"
    RCT = "rct"
    NON_RCT = "non_rct"
    PROSPECTIVE_COHORT = "prospective_cohort"
    RETROSPECTIVE_COHORT = "retrospective_cohort"
    CASE_CONTROL = "case_control"
    CROSS_SECTIONAL = "cross_sectional"
    CASE_SERIES = "case_series"
    NARRATIVE_REVIEW = "narrative_review"
    SYSTEMATIC_REVIEW = "systematic_review"
    SCOPING_REVIEW = "scoping_review"
    GUIDELINE = "guideline"
    OTHER = "other"

class RecordStatus(str, PyEnum):
    DRAFT = "draft"
    NORMAL = "normal"
    DELETED = "deleted"

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    hashed_password = Column(String(255), nullable=False)
    
    # 基本信息
    real_name = Column(String(50))
    avatar = Column(String(500))
    title = Column(String(50))  # 职称
    department = Column(String(100))  # 科室
    hospital = Column(String(100))  # 医院
    research_areas = Column(JSON, default=list)  # 研究领域标签
    disease_spectrum = Column(JSON, default=list)  # 疾病谱标签
    
    # 学术ID
    orcid = Column(String(50))
    
    # 角色和状态
    role = Column(Enum(UserRole), default=UserRole.DOCTOR)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # 通知设置
    notification_prefs = Column(JSON, default=dict)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # 关系
    literatures = relationship("Literature", back_populates="creator")
    collections = relationship("Collection", back_populates="user")

# 文献模型
class Literature(Base):
    __tablename__ = "literatures"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 基本信息
    title = Column(String(500), nullable=False)
    abstract = Column(Text)
    keywords = Column(JSON, default=list)
    diseases = Column(JSON, default=list)  # 关联疾病
    
    # 作者信息
    authors = Column(JSON, default=list)
    author_units = Column(JSON, default=list)
    first_author = Column(String(200))
    corresponding_author = Column(String(200))
    
    # 期刊信息
    journal = Column(String(200))
    year = Column(Integer)
    volume = Column(String(50))
    issue = Column(String(50))
    pages = Column(String(50))
    
    # 文献标识
    doi = Column(String(100), index=True)
    pmid = Column(String(50), index=True)
    
    # 分类
    literature_type = Column(Enum(LiteratureType))
    study_types = Column(JSON, default=list)  # 研究类型（可多选）
    
    # 来源和收录
    source = Column(String(50))  # PubMed, Web of Science等
    is_sci = Column(Boolean, default=False)
    level = Column(String(50))  # 南大核心/北大核心等
    cas_partition = Column(String(10))  # 中科院分区
    jcr_partition = Column(String(10))  # JCR分区
    impact_factor = Column(Numeric(5, 3))
    
    # 文本可用性
    text_availability = Column(String(20), default="abstract")  # full_text/abstract
    
    # 文件
    file_path = Column(String(500))
    file_size = Column(Integer)
    
    # 状态和权限
    status = Column(Enum(RecordStatus), default=RecordStatus.NORMAL)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = relationship("User", back_populates="literatures")
    collections = relationship("Collection", back_populates="literature")
    
    # 索引
    __table_args__ = (
        Index('idx_literature_title', 'title'),
        Index('idx_literature_journal', 'journal'),
        Index('idx_literature_year', 'year'),
        Index('idx_literature_status', 'status'),
    )

# 文献收藏模型
class Collection(Base):
    __tablename__ = "collections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    literature_id = Column(UUID(as_uuid=True), ForeignKey("literatures.id"))
    folder_path = Column(String(500), default="/")  # 文件夹路径
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="collections")
    literature = relationship("Literature", back_populates="collections")

# 阅读记录模型
class ReadingLog(Base):
    __tablename__ = "reading_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    literature_id = Column(UUID(as_uuid=True), ForeignKey("literatures.id"))
    read_at = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # 阅读时长（秒）
    page_number = Column(Integer)

# 回收站模型
class RecycleBin(Base):
    __tablename__ = "recycle_bins"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_type = Column(String(50), nullable=False)  # literature/user等
    record_id = Column(UUID(as_uuid=True), nullable=False)
    original_data = Column(JSON)
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    deleted_at = Column(DateTime, default=datetime.utcnow)
    auto_delete_at = Column(DateTime)  # 30天后自动删除
    status = Column(String(20), default="pending")  # pending/deleted/restored
