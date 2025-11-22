"""
Document schemas
"""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.project import DocumentType


# Word Document Schemas
class WordSection(BaseModel):
    """Word document section schema"""
    id: str = Field(..., description="Unique section identifier")
    title: str = Field(..., min_length=1, max_length=255, description="Section header/title")
    order: int = Field(..., ge=0, description="Section order/position")


class WordOutlineStructure(BaseModel):
    """Word document outline structure"""
    sections: List[WordSection] = Field(..., min_length=1, description="List of document sections")
    
    @field_validator('sections')
    @classmethod
    def validate_sections(cls, v: List[WordSection]) -> List[WordSection]:
        """Validate sections have unique IDs and orders"""
        if not v:
            raise ValueError('At least one section is required')
        
        section_ids = [s.id for s in v]
        if len(section_ids) != len(set(section_ids)):
            raise ValueError('Section IDs must be unique')
        
        orders = [s.order for s in v]
        if len(orders) != len(set(orders)):
            raise ValueError('Section orders must be unique')
        
        return sorted(v, key=lambda x: x.order)


# PowerPoint Document Schemas
class PowerPointSlide(BaseModel):
    """PowerPoint slide schema"""
    id: str = Field(..., description="Unique slide identifier")
    title: str = Field(..., min_length=1, max_length=255, description="Slide title")
    order: int = Field(..., ge=0, description="Slide order/position")


class PowerPointStructure(BaseModel):
    """PowerPoint document structure"""
    slides: List[PowerPointSlide] = Field(..., min_length=1, description="List of slides")
    
    @field_validator('slides')
    @classmethod
    def validate_slides(cls, v: List[PowerPointSlide]) -> List[PowerPointSlide]:
        """Validate slides have unique IDs and orders"""
        if not v:
            raise ValueError('At least one slide is required')
        
        slide_ids = [s.id for s in v]
        if len(slide_ids) != len(set(slide_ids)):
            raise ValueError('Slide IDs must be unique')
        
        orders = [s.order for s in v]
        if len(orders) != len(set(orders)):
            raise ValueError('Slide orders must be unique')
        
        return sorted(v, key=lambda x: x.order)


# Document Configuration Schemas
class DocumentConfigureRequest(BaseModel):
    """Schema for document configuration"""
    structure: Dict[str, Any] = Field(..., description="Document structure (Word outline or PowerPoint slides)")
    
    @field_validator('structure')
    @classmethod
    def validate_structure(cls, v: Dict[str, Any], info) -> Dict[str, Any]:
        """Validate structure based on document type"""
        # This will be validated in the service based on project document_type
        if not v:
            raise ValueError('Structure cannot be empty')
        return v


class DocumentStructureUpdate(BaseModel):
    """Schema for updating document structure"""
    structure: Dict[str, Any] = Field(..., description="Updated document structure")


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: UUID
    project_id: UUID
    structure: Dict[str, Any]
    content: Optional[Dict[str, Any]] = None
    version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# AI Template Generation Schemas
class AITemplateRequest(BaseModel):
    """Schema for AI template generation request"""
    main_topic: str = Field(..., min_length=1, max_length=500, description="Main topic for template generation")
    document_type: DocumentType = Field(..., description="Document type (word or powerpoint)")


class AITemplateResponse(BaseModel):
    """Schema for AI template generation response"""
    structure: Dict[str, Any] = Field(..., description="Generated document structure")
    suggestions: List[str] = Field(default_factory=list, description="Additional suggestions")

