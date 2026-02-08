"""
文献服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException
import uuid

from app.db.models import Literature, User, RecordStatus
from app.models.literature import LiteratureCreate, LiteratureUpdate, LiteratureSearch

class LiteratureService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, data: LiteratureCreate, user_id: uuid.UUID) -> Literature:
        db_literature = Literature(
            **data.dict(),
            created_by=user_id,
            status=RecordStatus.NORMAL
        )
        self.db.add(db_literature)
        self.db.commit()
        self.db.refresh(db_literature)
        return db_literature
    
    def get_by_id(self, literature_id: uuid.UUID) -> Optional[Literature]:
        return self.db.query(Literature).filter(
            Literature.id == literature_id,
            Literature.status == RecordStatus.NORMAL
        ).first()
    
    def search(
        self,
        search_params: LiteratureSearch,
        user_id: Optional[uuid.UUID] = None
    ) -> tuple[List[Literature], int]:
        query = self.db.query(Literature).filter(
            Literature.status == RecordStatus.NORMAL
        )
        
        # 关键词搜索
        if search_params.keyword:
            keyword_filter = or_(
                Literature.title.ilike(f"%{search_params.keyword}%"),
                Literature.abstract.ilike(f"%{search_params.keyword}%"),
            )
            query = query.filter(keyword_filter)
        
        # 疾病筛选
        if search_params.diseases:
            # JSONB数组包含查询
            for disease in search_params.diseases:
                query = query.filter(Literature.diseases.contains([disease]))
        
        # 文献类型筛选
        if search_params.literature_types:
            query = query.filter(Literature.literature_type.in_(search_params.literature_types))
        
        # 研究类型筛选
        if search_params.study_types:
            for study_type in search_params.study_types:
                query = query.filter(Literature.study_types.contains([study_type]))
        
        # 年份范围
        if search_params.year_from:
            query = query.filter(Literature.year >= search_params.year_from)
        if search_params.year_to:
            query = query.filter(Literature.year <= search_params.year_to)
        
        # SCI筛选
        if search_params.is_sci is not None:
            query = query.filter(Literature.is_sci == search_params.is_sci)
        
        # 统计总数
        total = query.count()
        
        # 分页
        offset = (search_params.page - 1) * search_params.page_size
        items = query.offset(offset).limit(search_params.page_size).all()
        
        return items, total
    
    def update(
        self,
        literature_id: uuid.UUID,
        data: LiteratureUpdate,
        user_id: uuid.UUID
    ) -> Literature:
        literature = self.get_by_id(literature_id)
        if not literature:
            raise HTTPException(status_code=404, detail="Literature not found")
        
        # 权限检查（只有创建者或管理员可以修改）
        if literature.created_by != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(literature, field, value)
        
        self.db.commit()
        self.db.refresh(literature)
        return literature
    
    def delete(self, literature_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        literature = self.get_by_id(literature_id)
        if not literature:
            raise HTTPException(status_code=404, detail="Literature not found")
        
        # 权限检查
        if literature.created_by != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # 逻辑删除
        literature.status = RecordStatus.DELETED
        self.db.commit()
        return True
