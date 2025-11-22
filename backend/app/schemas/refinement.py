"""
Refinement schemas
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.models.refinement import FeedbackType


class RefinementRequest(BaseModel):
    """Schema for refinement request with AI prompt"""
    section_id: str = Field(..., description="Section or slide ID to refine")
    refinement_prompt: str = Field(..., min_length=1, description="AI refinement prompt (e.g., 'Make this more formal', 'Convert to bullet points')")


class RefinementResponse(BaseModel):
    """
    Schema for refinement response.
    Content is stored in documents.content as the single source of truth.
    new_content is included in response for backward compatibility with frontend.
    """
    id: UUID
    document_id: UUID
    section_id: str
    refinement_prompt: Optional[str] = None
    previous_content: Optional[str] = None  # TEMPORARY: For backward compatibility
    new_content: Optional[str] = None  # TEMPORARY: Included for frontend compatibility
    feedback: Optional[FeedbackType] = None  # Deprecated - use FeedbackResponse instead
    comments: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackResponse(BaseModel):
    """Schema for feedback response"""
    id: UUID
    document_id: UUID
    section_id: str
    feedback_type: FeedbackType
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackRequest(BaseModel):
    """Schema for like/dislike feedback"""
    section_id: str = Field(..., description="Section or slide ID")
    feedback: Optional[FeedbackType] = Field(None, description="Like, dislike, or null to reset")


class CommentRequest(BaseModel):
    """Schema for adding comments"""
    section_id: str = Field(..., description="Section or slide ID")
    comments: str = Field(..., min_length=1, description="User comments")


class RefinementHistoryResponse(BaseModel):
    """Schema for refinement history response"""
    refinements: List[RefinementResponse]
    total: int
    section_id: Optional[str] = None

