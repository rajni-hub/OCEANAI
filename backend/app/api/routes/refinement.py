"""
Refinement routes
"""
from typing import Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict as TypingDict
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project, DocumentType
from app.models.refinement import FeedbackType
from app.schemas.refinement import (
    RefinementRequest,
    RefinementResponse,
    FeedbackRequest,
    FeedbackResponse,
    CommentRequest,
    RefinementHistoryResponse
)
from app.services.project_service import get_project_by_id
from app.services.refinement_service import (
    refine_section_with_ai,
    refine_slide_with_ai,
    submit_feedback,
    add_comment,
    get_refinement_history,
    get_refinement_count,
    get_feedback_for_sections
)

router = APIRouter()


@router.post(
    "/{project_id}/refine",
    response_model=RefinementResponse,
    status_code=status.HTTP_200_OK,
    summary="Refine section/slide with AI",
    description="Refine content for a section (Word) or slide (PowerPoint) using AI based on user prompt"
)
async def refine_content(
    project_id: UUID,
    refinement_request: RefinementRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refine content for a section or slide using AI
    
    - **project_id**: Project UUID
    - **section_id**: Section or slide ID to refine
    - **refinement_prompt**: AI refinement instruction (e.g., "Make this more formal", "Convert to bullet points")
    
    Returns the refinement record with updated content
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        # Log the refinement request for debugging
        print(f"[REFINEMENT] Project ID: {project_id}, Section ID: {refinement_request.section_id}, Prompt: {refinement_request.refinement_prompt[:50]}...")
        
        if project.document_type == DocumentType.WORD:
            refinement = refine_section_with_ai(
                db=db,
                project=project,
                user=current_user,
                section_id=refinement_request.section_id,
                refinement_prompt=refinement_request.refinement_prompt
            )
        else:  # powerpoint
            refinement = refine_slide_with_ai(
                db=db,
                project=project,
                user=current_user,
                slide_id=refinement_request.section_id,
                refinement_prompt=refinement_request.refinement_prompt
            )
        
        print(f"[REFINEMENT] Success - Section ID: {refinement.section_id}")
        return refinement
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refining content: {str(e)}"
        )


@router.post(
    "/{project_id}/feedback",
    response_model=Optional[FeedbackResponse],
    status_code=status.HTTP_200_OK,
    summary="Submit like/dislike feedback (YouTube-style toggle)",
    description="Submit like/dislike feedback with toggle logic. Clicking same button resets to neutral."
)
async def submit_section_feedback(
    project_id: UUID,
    feedback_request: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit like/dislike feedback with YouTube-style toggle behavior:
    - Clicking LIKE when already LIKE → resets to neutral (null)
    - Clicking DISLIKE when already DISLIKE → resets to neutral (null)
    - Clicking opposite → switches feedback value
    - Only ONE feedback row per section (UPDATE instead of INSERT)
    
    - **project_id**: Project UUID
    - **section_id**: Section or slide ID
    - **feedback**: "like", "dislike", or null to reset
    
    Returns the feedback record (or null if reset)
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        feedback_record = submit_feedback(
            db=db,
            project=project,
            user=current_user,
            section_id=feedback_request.section_id,
            feedback=feedback_request.feedback
        )
        return feedback_record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting feedback: {str(e)}"
        )


@router.post(
    "/{project_id}/comments",
    response_model=RefinementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add comments",
    description="Add comments for a section or slide"
)
async def add_section_comments(
    project_id: UUID,
    comment_request: CommentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add comments for a section or slide
    
    - **project_id**: Project UUID
    - **section_id**: Section or slide ID
    - **comments**: User comments text
    
    Returns the refinement record with comments
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        refinement = add_comment(
            db=db,
            project=project,
            user=current_user,
            section_id=comment_request.section_id,
            comments=comment_request.comments
        )
        return refinement
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding comments: {str(e)}"
        )


@router.get(
    "/{project_id}/refinement-history",
    response_model=RefinementHistoryResponse,
    summary="Get refinement history",
    description="Get refinement history for a document or specific section/slide"
)
async def get_project_refinement_history(
    project_id: UUID,
    section_id: Optional[str] = Query(None, description="Filter by section/slide ID"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=1000, description="Pagination limit"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get refinement history for a project
    
    - **project_id**: Project UUID
    - **section_id**: Optional section/slide ID to filter by
    - **skip**: Pagination offset
    - **limit**: Pagination limit
    
    Returns list of refinement records
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        refinements = get_refinement_history(
            db=db,
            project=project,
            user=current_user,
            section_id=section_id,
            skip=skip,
            limit=limit
        )
        
        total = get_refinement_count(
            db=db,
            project=project,
            user=current_user,
            section_id=section_id
        )
        
        return RefinementHistoryResponse(
            refinements=refinements,
            total=total,
            section_id=section_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting refinement history: {str(e)}"
        )


@router.get(
    "/{project_id}/refinement-history/{section_id}",
    response_model=RefinementHistoryResponse,
    summary="Get refinement history for section/slide",
    description="Get refinement history for a specific section or slide"
)
async def get_section_refinement_history(
    project_id: UUID,
    section_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get refinement history for a specific section or slide
    
    - **project_id**: Project UUID
    - **section_id**: Section or slide ID
    - **skip**: Pagination offset
    - **limit**: Pagination limit
    
    Returns list of refinement records for the section/slide
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        refinements = get_refinement_history(
            db=db,
            project=project,
            user=current_user,
            section_id=section_id,
            skip=skip,
            limit=limit
        )
        
        total = get_refinement_count(
            db=db,
            project=project,
            user=current_user,
            section_id=section_id
        )
        
        return RefinementHistoryResponse(
            refinements=refinements,
            total=total,
            section_id=section_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting refinement history: {str(e)}"
        )


@router.get(
    "/{project_id}/feedback",
    response_model=Dict[str, str],
    summary="Get feedback for sections",
    description="Get all feedback (likes/dislikes) for sections in a document"
)
async def get_project_feedback(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get feedback for all sections in a project.
    Returns a dictionary mapping section_id to feedback_type.
    
    - **project_id**: Project UUID
    
    Returns: { "section-1": "like", "section-2": "dislike", ... }
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        feedback_dict = get_feedback_for_sections(
            db=db,
            project=project,
            user=current_user
        )
        # Convert FeedbackType enum to string values
        return {k: v.value for k, v in feedback_dict.items()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting feedback: {str(e)}"
        )
