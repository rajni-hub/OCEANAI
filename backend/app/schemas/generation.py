"""
Generation schemas
"""
from pydantic import BaseModel
from typing import Dict, Optional


class GenerationResponse(BaseModel):
    """Schema for generation response"""
    message: str
    document_id: str
    total_items: int
    generated_items: int
    status: str


class SingleSectionGenerationRequest(BaseModel):
    """Schema for single section generation request"""
    section_id: str


class SingleSlideGenerationRequest(BaseModel):
    """Schema for single slide generation request"""
    slide_id: str


class GenerationStatusResponse(BaseModel):
    """Schema for generation status response"""
    status: str  # "not_configured", "partial", "completed"
    total_sections: Optional[int] = None
    generated_sections: Optional[int] = None
    total_slides: Optional[int] = None
    generated_slides: Optional[int] = None
    progress_percentage: int
    message: Optional[str] = None

