"""
Project schemas
"""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Union
from app.models.project import DocumentType


class ProjectBase(BaseModel):
    """Base project schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Project title")
    document_type: DocumentType = Field(..., description="Document type (word or powerpoint)")
    main_topic: str = Field(..., min_length=1, max_length=500, description="Main topic or prompt")
    
    @field_validator('title', 'main_topic')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Validate that string fields are not empty after stripping"""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class ProjectCreate(ProjectBase):
    """Schema for project creation"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for project update"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    main_topic: Optional[str] = Field(None, min_length=1, max_length=500)
    
    @field_validator('title', 'main_topic')
    @classmethod
    def validate_not_empty_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Validate that string fields are not empty if provided"""
        if v is not None:
            if not v.strip():
                raise ValueError('Field cannot be empty')
            return v.strip()
        return v


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for project list response with pagination"""
    projects: List[ProjectResponse]
    total: int
    skip: int
    limit: int

