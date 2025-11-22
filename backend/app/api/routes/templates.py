"""
Template API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    TemplateListResponse
)
from app.services.template_service import (
    create_template,
    get_template_by_id,
    get_templates_for_user,
    get_default_template,
    update_template,
    delete_template
)

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post(
    "",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create template",
    description="Create a new document template with custom styling"
)
async def create_template_endpoint(
    template_data: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new template
    
    Args:
        template_data: Template creation data
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Created template
    """
    try:
        template = create_template(
            db=db,
            user=current_user,
            template_data=template_data
        )
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating template: {str(e)}"
        )


@router.get(
    "",
    response_model=TemplateListResponse,
    summary="List templates",
    description="Get all templates for the current user, optionally filtered by document type"
)
async def list_templates(
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all templates for the current user
    
    Args:
        document_type: Optional filter by document type ("word" or "powerpoint")
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of templates
    """
    try:
        templates = get_templates_for_user(
            db=db,
            user=current_user,
            document_type=document_type
        )
        return TemplateListResponse(
            templates=templates,
            total=len(templates)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing templates: {str(e)}"
        )


@router.get(
    "/default",
    response_model=TemplateResponse,
    summary="Get default template",
    description="Get the default template for a document type"
)
async def get_default_template_endpoint(
    document_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get default template for a document type
    
    Args:
        document_type: Document type ("word" or "powerpoint")
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Default template or first available template
    """
    if document_type not in ["word", "powerpoint"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="document_type must be 'word' or 'powerpoint'"
        )
    
    try:
        template = get_default_template(
            db=db,
            user=current_user,
            document_type=document_type
        )
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No template found for document type: {document_type}"
            )
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting default template: {str(e)}"
        )


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Get template",
    description="Get a specific template by ID"
)
async def get_template(
    template_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get template by ID
    
    Args:
        template_id: Template UUID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Template object
    """
    try:
        template = get_template_by_id(
            db=db,
            template_id=template_id,
            user=current_user
        )
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting template: {str(e)}"
        )


@router.put(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Update template",
    description="Update an existing template"
)
async def update_template_endpoint(
    template_id: UUID,
    template_data: TemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update template
    
    Args:
        template_id: Template UUID
        template_data: Template update data
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated template
    """
    try:
        template = update_template(
            db=db,
            template_id=template_id,
            user=current_user,
            template_data=template_data
        )
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating template: {str(e)}"
        )


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete template",
    description="Delete a template"
)
async def delete_template_endpoint(
    template_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete template
    
    Args:
        template_id: Template UUID
        current_user: Authenticated user
        db: Database session
    """
    try:
        delete_template(
            db=db,
            template_id=template_id,
            user=current_user
        )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting template: {str(e)}"
        )

