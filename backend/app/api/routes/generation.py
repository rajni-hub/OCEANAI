"""
AI content generation routes
"""
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.generation import (
    GenerationResponse,
    SingleSectionGenerationRequest,
    SingleSlideGenerationRequest,
    GenerationStatusResponse
)
from app.schemas.document import DocumentResponse
from app.services.project_service import get_project_by_id
from app.services.generation_service import (
    generate_document_content,
    generate_single_section_content,
    generate_single_slide_content,
    get_generation_status
)

router = APIRouter()


@router.post(
    "/{project_id}/generate",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate document content",
    description="Generate content for all sections (Word) or slides (PowerPoint) in the document"
)
async def generate_project_content(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate content for all sections/slides in a document
    
    - **project_id**: Project UUID
    
    Returns the document with generated content for all sections/slides.
    This may take some time depending on the number of sections/slides.
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        document = generate_document_content(
            db=db,
            project=project,
            user=current_user
        )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )


@router.post(
    "/{project_id}/generate-section",
    response_model=Dict[str, str],
    summary="Generate single section content (Word)",
    description="Generate content for a single section in a Word document"
)
async def generate_single_section(
    project_id: UUID,
    request: SingleSectionGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate content for a single section (Word documents only)
    
    - **project_id**: Project UUID
    - **section_id**: Section ID to generate content for
    
    Returns the generated content for the specified section
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        content = generate_single_section_content(
            db=db,
            project=project,
            user=current_user,
            section_id=request.section_id
        )
        return content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating section content: {str(e)}"
        )


@router.post(
    "/{project_id}/generate-slide",
    response_model=Dict[str, str],
    summary="Generate single slide content (PowerPoint)",
    description="Generate content for a single slide in a PowerPoint document"
)
async def generate_single_slide(
    project_id: UUID,
    request: SingleSlideGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate content for a single slide (PowerPoint documents only)
    
    - **project_id**: Project UUID
    - **slide_id**: Slide ID to generate content for
    
    Returns the generated content for the specified slide
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        content = generate_single_slide_content(
            db=db,
            project=project,
            user=current_user,
            slide_id=request.slide_id
        )
        return content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating slide content: {str(e)}"
        )


@router.get(
    "/{project_id}/generation-status",
    response_model=GenerationStatusResponse,
    summary="Get generation status",
    description="Get the status of content generation for a document"
)
async def get_project_generation_status(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the status of content generation for a project
    
    - **project_id**: Project UUID
    
    Returns generation status including progress information
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        status_info = get_generation_status(
            db=db,
            project=project,
            user=current_user
        )
        return status_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting generation status: {str(e)}"
        )
