"""
Generation service - Business logic for content generation
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from uuid import UUID
from app.models.document import Document
from app.models.project import Project
from app.models.user import User
from app.services.project_service import get_project_by_id
from app.services.document_service import get_document
from app.services.ai_service import generate_all_content
from app.models.project import DocumentType


def generate_document_content(
    db: Session,
    project: Project,
    user: User
) -> Document:
    """
    Generate content for all sections/slides in a document
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user (for verification)
        
    Returns:
        Updated document with generated content
        
    Raises:
        HTTPException: If validation fails or generation fails
    """
    # Verify project belongs to user
    if project.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    # Get document
    document = get_document(db=db, project=project)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found. Please configure the document structure first."
        )
    
    # Verify document has structure
    structure = document.structure
    if not structure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document structure is empty. Please configure the structure first."
        )
    
    # Generate content based on document type
    try:
        generated_content = generate_all_content(
            main_topic=project.main_topic,
            structure=structure,
            document_type=project.document_type
        )
        
        # Update document content
        document.content = generated_content
        document.version += 1
        
        db.commit()
        db.refresh(document)
        
        return document
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AI generation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )


def generate_single_section_content(
    db: Session,
    project: Project,
    user: User,
    section_id: str
) -> Dict[str, str]:
    """
    Generate content for a single section (Word documents only)
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Section ID to generate content for
        
    Returns:
        Dictionary with section_id and generated content
        
    Raises:
        HTTPException: If validation fails or generation fails
    """
    if project.document_type != DocumentType.WORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Single section generation is only available for Word documents"
        )
    
    # Verify project belongs to user
    if project.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    # Get document
    document = get_document(db=db, project=project)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    structure = document.structure
    sections = structure.get("sections", [])
    
    # Find the section
    section = None
    for sec in sections:
        if sec.get("id") == section_id:
            section = sec
            break
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section '{section_id}' not found in document structure"
        )
    
    # Get previous sections for context
    sorted_sections = sorted(sections, key=lambda x: x.get("order", 0))
    current_order = section.get("order", 0)
    previous_titles = [
        s.get("title") for s in sorted_sections
        if s.get("order", 0) < current_order
    ]
    
    # Generate content
    try:
        from app.services.ai_service import generate_section_content
        
        content = generate_section_content(
            main_topic=project.main_topic,
            section_title=section.get("title", ""),
            section_id=section_id,
            previous_sections=previous_titles if previous_titles else None
        )
        
        # Update document content
        if not document.content:
            document.content = {}
        
        document.content[section_id] = content
        document.version += 1
        
        db.commit()
        db.refresh(document)
        
        return {
            section_id: content
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating section content: {str(e)}"
        )


def generate_single_slide_content(
    db: Session,
    project: Project,
    user: User,
    slide_id: str
) -> Dict[str, str]:
    """
    Generate content for a single slide (PowerPoint documents only)
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        slide_id: Slide ID to generate content for
        
    Returns:
        Dictionary with slide_id and generated content
        
    Raises:
        HTTPException: If validation fails or generation fails
    """
    if project.document_type != DocumentType.POWERPOINT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Single slide generation is only available for PowerPoint documents"
        )
    
    # Verify project belongs to user
    if project.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    # Get document
    document = get_document(db=db, project=project)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    structure = document.structure
    slides = structure.get("slides", [])
    
    # Find the slide
    slide = None
    for sl in slides:
        if sl.get("id") == slide_id:
            slide = sl
            break
    
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slide '{slide_id}' not found in document structure"
        )
    
    # Get previous slides for context
    sorted_slides = sorted(slides, key=lambda x: x.get("order", 0))
    current_order = slide.get("order", 0)
    previous_titles = [
        s.get("title") for s in sorted_slides
        if s.get("order", 0) < current_order
    ]
    
    # Generate content
    try:
        from app.services.ai_service import generate_slide_content
        
        content = generate_slide_content(
            main_topic=project.main_topic,
            slide_title=slide.get("title", ""),
            slide_id=slide_id,
            previous_slides=previous_titles if previous_titles else None
        )
        
        # Update document content
        if not document.content:
            document.content = {}
        
        document.content[slide_id] = content
        document.version += 1
        
        db.commit()
        db.refresh(document)
        
        return {
            slide_id: content
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating slide content: {str(e)}"
        )


def get_generation_status(
    db: Session,
    project: Project,
    user: User
) -> Dict[str, Any]:
    """
    Get the status of content generation for a document
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        
    Returns:
        Dictionary with generation status information
    """
    # Verify project belongs to user
    if project.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    document = get_document(db=db, project=project)
    
    if not document:
        return {
            "status": "not_configured",
            "message": "Document structure not configured yet"
        }
    
    structure = document.structure
    content = document.content or {}
    
    if project.document_type == DocumentType.WORD:
        sections = structure.get("sections", [])
        total_sections = len(sections)
        generated_sections = len([sid for sid in content.keys() if sid.startswith("section-")])
        
        return {
            "status": "completed" if generated_sections == total_sections else "partial",
            "total_sections": total_sections,
            "generated_sections": generated_sections,
            "progress_percentage": int((generated_sections / total_sections * 100)) if total_sections > 0 else 0
        }
    else:  # POWERPOINT
        slides = structure.get("slides", [])
        total_slides = len(slides)
        generated_slides = len([sid for sid in content.keys() if sid.startswith("slide-")])
        
        return {
            "status": "completed" if generated_slides == total_slides else "partial",
            "total_slides": total_slides,
            "generated_slides": generated_slides,
            "progress_percentage": int((generated_slides / total_slides * 100)) if total_slides > 0 else 0
        }

