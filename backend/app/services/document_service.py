"""
Document service - Business logic for document configuration
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, Optional, Union
from uuid import UUID
from app.models.document import Document
from app.models.project import Project, DocumentType
from app.models.user import User
from app.schemas.document import (
    WordOutlineStructure,
    PowerPointStructure,
    DocumentConfigureRequest,
    DocumentStructureUpdate
)


def validate_word_structure(structure: Dict[str, Any]) -> bool:
    """
    Validate Word document structure
    
    Args:
        structure: Document structure dictionary
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: If structure is invalid
    """
    if "sections" not in structure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word document structure must contain 'sections' array"
        )
    
    sections = structure["sections"]
    if not isinstance(sections, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'sections' must be an array"
        )
    
    if len(sections) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word document must have at least one section"
        )
    
    # Validate each section
    section_ids = set()
    orders = set()
    
    for i, section in enumerate(sections):
        if not isinstance(section, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} must be an object"
            )
        
        if "id" not in section or "title" not in section or "order" not in section:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} must contain 'id', 'title', and 'order' fields"
            )
        
        section_id = section["id"]
        if not isinstance(section_id, str) or len(section_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} 'id' must be a non-empty string"
            )
        
        if section_id in section_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate section ID: {section_id}"
            )
        section_ids.add(section_id)
        
        title = section["title"]
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} 'title' must be a non-empty string"
            )
        
        if len(title) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} 'title' must be less than 255 characters"
            )
        
        order = section["order"]
        if not isinstance(order, int) or order < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {i} 'order' must be a non-negative integer"
            )
        
        if order in orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate section order: {order}"
            )
        orders.add(order)
    
    return True


def validate_powerpoint_structure(structure: Dict[str, Any]) -> bool:
    """
    Validate PowerPoint document structure
    
    Args:
        structure: Document structure dictionary
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: If structure is invalid
    """
    if "slides" not in structure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PowerPoint document structure must contain 'slides' array"
        )
    
    slides = structure["slides"]
    if not isinstance(slides, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'slides' must be an array"
        )
    
    if len(slides) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PowerPoint document must have at least one slide"
        )
    
    # Validate each slide
    slide_ids = set()
    orders = set()
    
    for i, slide in enumerate(slides):
        if not isinstance(slide, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} must be an object"
            )
        
        if "id" not in slide or "title" not in slide or "order" not in slide:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} must contain 'id', 'title', and 'order' fields"
            )
        
        slide_id = slide["id"]
        if not isinstance(slide_id, str) or len(slide_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} 'id' must be a non-empty string"
            )
        
        if slide_id in slide_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate slide ID: {slide_id}"
            )
        slide_ids.add(slide_id)
        
        title = slide["title"]
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} 'title' must be a non-empty string"
            )
        
        if len(title) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} 'title' must be less than 255 characters"
            )
        
        order = slide["order"]
        if not isinstance(order, int) or order < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slide {i} 'order' must be a non-negative integer"
            )
        
        if order in orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate slide order: {order}"
            )
        orders.add(order)
    
    return True


def validate_document_structure(
    structure: Dict[str, Any],
    document_type: DocumentType
) -> bool:
    """
    Validate document structure based on document type
    
    Args:
        structure: Document structure dictionary
        document_type: Type of document (word or powerpoint)
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: If structure is invalid
    """
    if document_type == DocumentType.WORD:
        return validate_word_structure(structure)
    elif document_type == DocumentType.POWERPOINT:
        return validate_powerpoint_structure(structure)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type: {document_type}"
        )


def get_or_create_document(
    db: Session,
    project: Project
) -> Document:
    """
    Get existing document or create a new one for the project
    
    Args:
        db: Database session
        project: Project object
        
    Returns:
        Document object
    """
    document = db.query(Document).filter(Document.project_id == project.id).first()
    
    if not document:
        # Create default structure based on document type
        if project.document_type == DocumentType.WORD:
            default_structure = {
                "sections": [
                    {
                        "id": "section-1",
                        "title": "Introduction",
                        "order": 0
                    }
                ]
            }
        else:  # POWERPOINT
            default_structure = {
                "slides": [
                    {
                        "id": "slide-1",
                        "title": "Title Slide",
                        "order": 0
                    }
                ]
            }
        
        document = Document(
            project_id=project.id,
            structure=default_structure,
            version=1
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    
    return document


def configure_document(
    db: Session,
    project: Project,
    config_request: DocumentConfigureRequest
) -> Document:
    """
    Configure document structure for a project
    
    Args:
        db: Database session
        project: Project object
        config_request: Configuration request
        
    Returns:
        Updated document object
        
    Raises:
        HTTPException: If validation fails
    """
    # Validate structure based on document type
    validate_document_structure(
        structure=config_request.structure,
        document_type=project.document_type
    )
    
    # Get or create document
    document = get_or_create_document(db=db, project=project)
    
    # Update structure and increment version
    document.structure = config_request.structure
    document.version += 1
    
    db.commit()
    db.refresh(document)
    
    return document


def update_document_structure(
    db: Session,
    project: Project,
    structure_update: DocumentStructureUpdate
) -> Document:
    """
    Update document structure
    
    Args:
        db: Database session
        project: Project object
        structure_update: Structure update request
        
    Returns:
        Updated document object
        
    Raises:
        HTTPException: If validation fails or document not found
    """
    document = db.query(Document).filter(Document.project_id == project.id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found. Please configure the document first."
        )
    
    # Validate structure
    validate_document_structure(
        structure=structure_update.structure,
        document_type=project.document_type
    )
    
    # Update structure and increment version
    document.structure = structure_update.structure
    document.version += 1
    
    db.commit()
    db.refresh(document)
    
    return document


def get_document(
    db: Session,
    project: Project
) -> Optional[Document]:
    """
    Get document for a project
    
    Args:
        db: Database session
        project: Project object
        
    Returns:
        Document object or None if not found
    """
    return db.query(Document).filter(Document.project_id == project.id).first()


def reorder_sections(
    db: Session,
    project: Project,
    section_orders: Dict[str, int]
) -> Document:
    """
    Reorder sections in a Word document
    
    Args:
        db: Database session
        project: Project object
        section_orders: Dictionary mapping section IDs to new orders
        
    Returns:
        Updated document object
        
    Raises:
        HTTPException: If document not found or invalid
    """
    if project.document_type != DocumentType.WORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reorder sections is only available for Word documents"
        )
    
    document = get_document(db=db, project=project)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    structure = document.structure.copy()
    sections = structure.get("sections", [])
    
    # Update orders
    for section in sections:
        section_id = section.get("id")
        if section_id in section_orders:
            section["order"] = section_orders[section_id]
    
    # Validate updated structure
    validate_word_structure(structure)
    
    # Update document
    document.structure = structure
    document.version += 1
    
    db.commit()
    db.refresh(document)
    
    return document


def reorder_slides(
    db: Session,
    project: Project,
    slide_orders: Dict[str, int]
) -> Document:
    """
    Reorder slides in a PowerPoint document
    
    Args:
        db: Database session
        project: Project object
        slide_orders: Dictionary mapping slide IDs to new orders
        
    Returns:
        Updated document object
        
    Raises:
        HTTPException: If document not found or invalid
    """
    if project.document_type != DocumentType.POWERPOINT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reorder slides is only available for PowerPoint documents"
        )
    
    document = get_document(db=db, project=project)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    structure = document.structure.copy()
    slides = structure.get("slides", [])
    
    # Update orders
    for slide in slides:
        slide_id = slide.get("id")
        if slide_id in slide_orders:
            slide["order"] = slide_orders[slide_id]
    
    # Validate updated structure
    validate_powerpoint_structure(structure)
    
    # Update document
    document.structure = structure
    document.version += 1
    
    db.commit()
    db.refresh(document)
    
    return document
