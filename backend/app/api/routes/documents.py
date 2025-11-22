"""
Document configuration routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.document import (
    DocumentConfigureRequest,
    DocumentStructureUpdate,
    DocumentResponse,
    AITemplateRequest,
    AITemplateResponse
)
from app.services.document_service import (
    configure_document,
    update_document_structure,
    get_document,
    reorder_sections,
    reorder_slides,
    get_or_create_document
)
from app.services.project_service import get_project_by_id
from app.services.ai_service import generate_template

router = APIRouter()


@router.post(
    "/{project_id}/configure",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Configure document structure",
    description="Configure or update the document structure (Word outline or PowerPoint slides)"
)
async def configure_project_document(
    project_id: UUID,
    config_request: DocumentConfigureRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Configure document structure for a project
    
    - **project_id**: Project UUID
    - **structure**: Document structure (Word sections or PowerPoint slides)
    
    Returns the configured document
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        document = configure_document(
            db=db,
            project=project,
            config_request=config_request
        )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error configuring document: {str(e)}"
        )


@router.get(
    "/{project_id}/document",
    response_model=DocumentResponse,
    summary="Get document configuration",
    description="Get the document structure and content for a project"
)
async def get_project_document(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document configuration for a project
    
    - **project_id**: Project UUID
    
    Returns the document structure and content
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    document = get_document(db=db, project=project)
    
    if not document:
        # Return a default structure if document doesn't exist yet
        document = get_or_create_document(db=db, project=project)
    
    return document


@router.put(
    "/{project_id}/document/structure",
    response_model=DocumentResponse,
    summary="Update document structure",
    description="Update the document structure (Word outline or PowerPoint slides)"
)
async def update_project_document_structure(
    project_id: UUID,
    structure_update: DocumentStructureUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update document structure for a project
    
    - **project_id**: Project UUID
    - **structure**: Updated document structure
    
    Returns the updated document
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        document = update_document_structure(
            db=db,
            project=project,
            structure_update=structure_update
        )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating document structure: {str(e)}"
        )


@router.post(
    "/{project_id}/document/reorder-sections",
    response_model=DocumentResponse,
    summary="Reorder Word document sections",
    description="Reorder sections in a Word document (Word documents only)"
)
async def reorder_document_sections(
    project_id: UUID,
    section_orders: Dict[str, int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reorder sections in a Word document
    
    - **project_id**: Project UUID
    - **section_orders**: Dictionary mapping section IDs to new order numbers
    
    Returns the updated document
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        document = reorder_sections(
            db=db,
            project=project,
            section_orders=section_orders
        )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reordering sections: {str(e)}"
        )


@router.post(
    "/{project_id}/document/reorder-slides",
    response_model=DocumentResponse,
    summary="Reorder PowerPoint slides",
    description="Reorder slides in a PowerPoint document (PowerPoint documents only)"
)
async def reorder_document_slides(
    project_id: UUID,
    slide_orders: Dict[str, int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reorder slides in a PowerPoint document
    
    - **project_id**: Project UUID
    - **slide_orders**: Dictionary mapping slide IDs to new order numbers
    
    Returns the updated document
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        document = reorder_slides(
            db=db,
            project=project,
            slide_orders=slide_orders
        )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reordering slides: {str(e)}"
        )


@router.post(
    "/{project_id}/ai-suggest-template",
    response_model=AITemplateResponse,
    summary="Generate AI template (Bonus)",
    description="Generate document structure using AI based on main topic (Bonus feature)"
)
async def generate_ai_template(
    project_id: UUID,
    template_request: AITemplateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate document template using AI (Bonus feature)
    
    - **project_id**: Project UUID
    - **main_topic**: Main topic for template generation
    - **document_type**: Document type (word or powerpoint)
    
    Returns generated structure that can be used for configuration
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Verify document type matches
    if project.document_type != template_request.document_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document type mismatch. Project is {project.document_type}, but request is {template_request.document_type}"
        )
    
    try:
        structure = generate_template(
            main_topic=template_request.main_topic,
            document_type=template_request.document_type
        )
        
        return AITemplateResponse(
            structure=structure,
            suggestions=[
                "You can customize the generated structure before applying it",
                "Add or remove sections/slides as needed",
                "Edit titles to match your requirements"
            ]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating template: {str(e)}"
        )
