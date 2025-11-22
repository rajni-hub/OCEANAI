"""
Template service - Business logic for template management
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from uuid import UUID
import json

from app.models.template import Template
from app.models.user import User
from app.schemas.template import TemplateCreate, TemplateUpdate


def create_template(
    db: Session,
    user: User,
    template_data: TemplateCreate
) -> Template:
    """
    Create a new template for a user
    
    Args:
        db: Database session
        user: User object
        template_data: Template creation data
        
    Returns:
        Created Template object
        
    Raises:
        HTTPException: If validation fails or creation fails
    """
    try:
        # If this is set as default, unset other defaults for same document type
        if template_data.is_default:
            db.query(Template).filter(
                Template.user_id == user.id,
                Template.document_type == template_data.document_type
            ).update({"is_default": False})
        
        # Convert Pydantic model to dict for JSON storage
        config_dict = template_data.config.model_dump()
        
        # Create template
        template = Template(
            user_id=user.id,
            name=template_data.name,
            description=template_data.description,
            document_type=template_data.document_type,
            config=config_dict,
            is_default=template_data.is_default,
            is_public=template_data.is_public
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return template
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating template: {str(e)}"
        )


def get_template_by_id(
    db: Session,
    template_id: UUID,
    user: User
) -> Optional[Template]:
    """
    Get template by ID (must belong to user)
    
    Args:
        db: Database session
        template_id: Template UUID
        user: User object
        
    Returns:
        Template object or None
        
    Raises:
        HTTPException: If template not found or access denied
    """
    template = db.query(Template).filter(Template.id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Handle SQLite string IDs vs PostgreSQL UUID objects
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        if str(template.user_id) != str(user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Template does not belong to user"
            )
    else:
        if template.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Template does not belong to user"
            )
    
    return template


def get_templates_for_user(
    db: Session,
    user: User,
    document_type: Optional[str] = None
) -> List[Template]:
    """
    Get all templates for a user
    
    Args:
        db: Database session
        user: User object
        document_type: Optional filter by document type
        
    Returns:
        List of Template objects
    """
    query = db.query(Template).filter(Template.user_id == user.id)
    
    if document_type:
        query = query.filter(Template.document_type == document_type)
    
    return query.order_by(Template.is_default.desc(), Template.created_at.desc()).all()


def get_default_template(
    db: Session,
    user: User,
    document_type: str
) -> Optional[Template]:
    """
    Get default template for a user and document type
    
    Args:
        db: Database session
        user: User object
        document_type: Document type ("word" or "powerpoint")
        
    Returns:
        Default Template object or None
    """
    # Handle SQLite string IDs vs PostgreSQL UUID objects
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        query = db.query(Template).filter(
            Template.user_id == str(user.id),
            Template.document_type == document_type,
            Template.is_default == True
        )
    else:
        query = db.query(Template).filter(
            Template.user_id == user.id,
            Template.document_type == document_type,
            Template.is_default == True
        )
    
    template = query.first()
    
    # If no default, get first template for this document type
    if not template:
        templates = get_templates_for_user(db, user, document_type)
        if templates:
            return templates[0]
    
    return template


def update_template(
    db: Session,
    template_id: UUID,
    user: User,
    template_data: TemplateUpdate
) -> Template:
    """
    Update an existing template
    
    Args:
        db: Database session
        template_id: Template UUID
        user: User object
        template_data: Template update data
        
    Returns:
        Updated Template object
        
    Raises:
        HTTPException: If template not found or update fails
    """
    template = get_template_by_id(db, template_id, user)
    
    try:
        # Update fields if provided
        if template_data.name is not None:
            template.name = template_data.name
        if template_data.description is not None:
            template.description = template_data.description
        if template_data.config is not None:
            template.config = template_data.config.model_dump()
        if template_data.is_public is not None:
            template.is_public = template_data.is_public
        
        # Handle default flag - if setting to True, unset others
        if template_data.is_default is not None:
            if template_data.is_default:
                db.query(Template).filter(
                    Template.user_id == user.id,
                    Template.document_type == template.document_type,
                    Template.id != template.id
                ).update({"is_default": False})
            template.is_default = template_data.is_default
        
        db.commit()
        db.refresh(template)
        
        return template
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating template: {str(e)}"
        )


def delete_template(
    db: Session,
    template_id: UUID,
    user: User
) -> bool:
    """
    Delete a template
    
    Args:
        db: Database session
        template_id: Template UUID
        user: User object
        
    Returns:
        True if deleted successfully
        
    Raises:
        HTTPException: If template not found or deletion fails
    """
    template = get_template_by_id(db, template_id, user)
    
    try:
        db.delete(template)
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting template: {str(e)}"
        )


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Convert hex color to RGB tuple
    
    Args:
        hex_color: Hex color string (e.g., "#1E40AF")
        
    Returns:
        Tuple of (R, G, B) integers
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_template_config(template: Template) -> Dict[str, Any]:
    """
    Get template configuration as dictionary
    
    Args:
        template: Template object
        
    Returns:
        Template configuration dictionary
    """
    return template.config if isinstance(template.config, dict) else json.loads(template.config)

