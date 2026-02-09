"""
项目服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from app.db.models import Project, User
from app.models.project import ProjectCreate, ProjectUpdate, ProjectStatus

class ProjectService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, data: ProjectCreate, user_id: uuid.UUID) -> Project:
        db_project = Project(
            **data.dict(),
            created_by=user_id
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_user_projects(
        self,
        user_id: uuid.UUID,
        status: Optional[ProjectStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Project], int]:
        query = self.db.query(Project).filter(
            (Project.created_by == user_id) |
            (Project.members.any(lambda m: m['user_id'] == str(user_id)))
        )
        
        if status:
            query = query.filter(Project.status == status)
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def update(
        self,
        project_id: uuid.UUID,
        data: ProjectUpdate,
        user_id: uuid.UUID
    ) -> Project:
        project = self.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if project.created_by != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(project, field, value)
        
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def delete(self, project_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        project = self.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if project.created_by != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        self.db.delete(project)
        self.db.commit()
        return True
