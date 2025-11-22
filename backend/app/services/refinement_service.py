"""
Refinement service - Business logic for content refinement
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, Optional, List
from uuid import UUID
from app.models.document import Document
from app.models.refinement import Refinement, Feedback, FeedbackType
from app.models.project import Project
from app.models.user import User
from app.services.project_service import get_project_by_id
from app.services.document_service import get_document
from app.models.project import DocumentType
from app.core.config import settings


def _limit_refinement_history(
    db: Session,
    document_id: UUID,
    section_id: str,
    max_refinements: int = 3
) -> None:
    """
    Limit refinement history to last N refinements per section.
    This prevents uncontrolled growth of the refinements table.
    
    Args:
        db: Database session
        document_id: Document UUID
        section_id: Section/slide ID
        max_refinements: Maximum number of refinements to keep (default: 3)
    """
    # Get all refinements for this section, ordered by created_at descending
    refinements = db.query(Refinement).filter(
        Refinement.document_id == document_id,
        Refinement.section_id == section_id
    ).order_by(Refinement.created_at.desc()).all()
    
    # If we have more than max_refinements, delete the oldest ones
    if len(refinements) > max_refinements:
        refinements_to_delete = refinements[max_refinements:]
        for refinement in refinements_to_delete:
            db.delete(refinement)
        print(f"[LIMIT_HISTORY] Deleted {len(refinements_to_delete)} old refinements for section {section_id}")


def refine_section_with_ai(
    db: Session,
    project: Project,
    user: User,
    section_id: str,
    refinement_prompt: str
) -> Refinement:
    """
    Refine a section using AI based on user's refinement prompt
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Section ID to refine
        refinement_prompt: User's refinement instruction
        
    Returns:
        Created refinement record
        
    Raises:
        HTTPException: If validation fails or generation fails
    """
    if project.document_type != DocumentType.WORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section refinement is only available for Word documents"
        )
    
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
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
    
    # Get current content
    content = document.content or {}
    print(f"[REFINE_SECTION] Looking for section_id: {section_id}")
    print(f"[REFINE_SECTION] Available content keys: {list(content.keys())}")
    
    previous_content = content.get(section_id, "")
    
    if not previous_content:
        print(f"[REFINE_SECTION] ERROR: Section '{section_id}' has no content")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Section '{section_id}' has no content to refine. Please generate content first."
        )
    
    print(f"[REFINE_SECTION] Found content for section, length: {len(previous_content)}")
    
    # Get section info from structure
    structure = document.structure
    sections = structure.get("sections", [])
    print(f"[REFINE_SECTION] Available sections: {[s.get('id') for s in sections]}")
    
    section = None
    for sec in sections:
        if sec.get("id") == section_id:
            section = sec
            break
    
    if not section:
        print(f"[REFINE_SECTION] ERROR: Section '{section_id}' not found in structure")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section '{section_id}' not found in document structure"
        )
    
    print(f"[REFINE_SECTION] Found section: {section.get('title')}")
    
    # Generate refined content using AI
    try:
        from app.services.ai_service import initialize_gemini
        import google.generativeai as genai
        
        model = initialize_gemini()
        
        # Build context-aware prompt
        section_title = section.get("title", "")
        prompt = f"""Refine the following content based on the user's request.

Original Section Title: {section_title}
Original Content:
{previous_content}

User's Refinement Request: {refinement_prompt}

Main Document Topic: {project.main_topic}

Please refine the content according to the user's request while maintaining relevance to the main topic and section title. Return only the refined content, without any additional explanation or formatting."""

        print(f"[REFINE_SECTION] Calling Gemini API...")
        print(f"[REFINE_SECTION] Prompt length: {len(prompt)}")
        print(f"[REFINE_SECTION] Previous content length: {len(previous_content)}")
        
        response = model.generate_content(prompt)
        new_content = response.text.strip()
        
        print(f"[REFINE_SECTION] Gemini API response received")
        print(f"[REFINE_SECTION] Raw response length: {len(response.text) if response.text else 0}")
        print(f"[REFINE_SECTION] Stripped content length: {len(new_content)}")
        print(f"[REFINE_SECTION] New content preview: {new_content[:200]}...")
        
        if not new_content:
            raise ValueError("Generated refined content is empty")
        
        print(f"[REFINE_SECTION] AI generated new content successfully, length: {len(new_content)}")
        
    except Exception as e:
        print(f"[REFINE_SECTION] ERROR in AI generation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating refined content: {str(e)}"
        )
    
    # Create refinement record (metadata only - content is in documents.content)
    # TEMPORARY: Populate new_content for frontend compatibility until migration is run
    refinement = Refinement(
        document_id=document.id,
        section_id=section_id,
        refinement_prompt=refinement_prompt,
        previous_content=previous_content,  # TEMPORARY: For frontend compatibility
        new_content=new_content  # TEMPORARY: Include in response for frontend
        # After migration, these fields will be removed - content is stored in documents.content
    )
    
    db.add(refinement)
    
    # Update document content
    # CRITICAL: Create a new dict to ensure SQLAlchemy detects the change
    # SQLAlchemy might not detect in-place modifications to JSON columns
    updated_content = content.copy()
    updated_content[section_id] = new_content
    
    print(f"[REFINE_SECTION] Before update - Content keys: {list(content.keys())}")
    print(f"[REFINE_SECTION] Updating section_id: {section_id}")
    print(f"[REFINE_SECTION] New content length: {len(new_content)}")
    
    # Assign new dict to trigger SQLAlchemy change detection
    document.content = updated_content
    document.version += 1
    
    print(f"[REFINE_SECTION] After update - Content keys: {list(document.content.keys())}")
    print(f"[REFINE_SECTION] Content for {section_id} exists: {section_id in document.content}")
    if section_id in document.content:
        print(f"[REFINE_SECTION] Content preview: {document.content[section_id][:100]}...")
    
    # Commit changes
    db.commit()
    print(f"[REFINE_SECTION] Database commit successful")
    
    # Refresh to get latest state
    db.refresh(document)
    db.refresh(refinement)
    
    print(f"[REFINE_SECTION] After refresh - Content keys: {list(document.content.keys())}")
    print(f"[REFINE_SECTION] Refinement saved successfully, section_id: {refinement.section_id}")
    print(f"[REFINE_SECTION] Document version: {document.version}")
    
    return refinement


def refine_slide_with_ai(
    db: Session,
    project: Project,
    user: User,
    slide_id: str,
    refinement_prompt: str
) -> Refinement:
    """
    Refine a slide using AI based on user's refinement prompt
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        slide_id: Slide ID to refine
        refinement_prompt: User's refinement instruction
        
    Returns:
        Created refinement record
        
    Raises:
        HTTPException: If validation fails or generation fails
    """
    if project.document_type != DocumentType.POWERPOINT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slide refinement is only available for PowerPoint documents"
        )
    
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
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
    
    # Get current content
    content = document.content or {}
    previous_content = content.get(slide_id, "")
    
    if not previous_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slide '{slide_id}' has no content to refine. Please generate content first."
        )
    
    # Get slide info from structure
    structure = document.structure
    slides = structure.get("slides", [])
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
    
    # Generate refined content using AI
    try:
        from app.services.ai_service import initialize_gemini
        
        model = initialize_gemini()
        
        # Build context-aware prompt
        slide_title = slide.get("title", "")
        prompt = f"""Refine the following slide content based on the user's request.

Original Slide Title: {slide_title}
Original Content:
{previous_content}

User's Refinement Request: {refinement_prompt}

Main Presentation Topic: {project.main_topic}

Please refine the content according to the user's request while maintaining relevance to the main topic and slide title. Keep it concise and suitable for a presentation slide. Return only the refined content, without any additional explanation or formatting."""

        response = model.generate_content(prompt)
        new_content = response.text.strip()
        
        if not new_content:
            raise ValueError("Generated refined content is empty")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating refined content: {str(e)}"
        )
    
    # Create refinement record (metadata only - content is in documents.content)
    # TEMPORARY: Populate new_content for frontend compatibility until migration is run
    refinement = Refinement(
        document_id=document.id,
        section_id=slide_id,
        refinement_prompt=refinement_prompt,
        previous_content=previous_content,  # TEMPORARY: For frontend compatibility
        new_content=new_content  # TEMPORARY: Include in response for frontend
        # After migration, these fields will be removed - content is stored in documents.content
    )
    
    db.add(refinement)
    
    # Update document content
    # CRITICAL: Create a new dict to ensure SQLAlchemy detects the change
    updated_content = content.copy()
    updated_content[slide_id] = new_content
    
    print(f"[REFINE_SLIDE] Before update - Content keys: {list(content.keys())}")
    print(f"[REFINE_SLIDE] Updating slide_id: {slide_id}")
    print(f"[REFINE_SLIDE] New content length: {len(new_content)}")
    
    # Assign new dict to trigger SQLAlchemy change detection
    document.content = updated_content
    document.version += 1
    
    # Limit refinement history to last 3 per section to prevent uncontrolled growth
    _limit_refinement_history(db, document.id, slide_id, max_refinements=3)
    
    print(f"[REFINE_SLIDE] After update - Content keys: {list(document.content.keys())}")
    
    # Commit changes
    db.commit()
    print(f"[REFINE_SLIDE] Database commit successful")
    
    # Refresh to get latest state
    db.refresh(document)
    db.refresh(refinement)
    
    print(f"[REFINE_SLIDE] Refinement saved successfully, slide_id: {refinement.section_id}")
    
    return refinement


def submit_feedback(
    db: Session,
    project: Project,
    user: User,
    section_id: str,
    feedback: Optional[FeedbackType]
) -> Optional[Feedback]:
    """
    Submit like/dislike feedback for a section/slide
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Section or slide ID
        feedback: Like or dislike
        
    Returns:
        Created refinement record with feedback
    """
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
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
    
    # Get current content
    content = document.content or {}
    current_content = content.get(section_id, "")
    
    if not current_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Section/slide '{section_id}' has no content"
        )
    
    # Use separate Feedback model for better separation of concerns
    # YouTube-style toggle logic: Only ONE feedback row per section
    # Check if feedback already exists for this section
    existing_feedback = db.query(Feedback).filter(
        Feedback.document_id == document.id,
        Feedback.section_id == section_id
    ).first()
    
    if feedback is None:
        # Reset to neutral - delete existing feedback if it exists
        if existing_feedback:
            db.delete(existing_feedback)
            db.commit()
            print(f"[FEEDBACK] Feedback reset to neutral for section {section_id}")
        return None
    else:
        # Set or update feedback
        if existing_feedback:
            # Update existing feedback (no duplicate inserts)
            existing_feedback.feedback_type = feedback
            existing_feedback.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_feedback)
            print(f"[FEEDBACK] Feedback updated: {section_id} -> {feedback.value}")
            return existing_feedback
        else:
            # Create new feedback record (only if none exists)
            feedback_record = Feedback(
                document_id=document.id,
                section_id=section_id,
                feedback_type=feedback
            )
            db.add(feedback_record)
            db.commit()
            db.refresh(feedback_record)
            print(f"[FEEDBACK] Feedback created: {section_id} -> {feedback.value}")
            return feedback_record


def add_comment(
    db: Session,
    project: Project,
    user: User,
    section_id: str,
    comments: str
) -> Refinement:
    """
    Add comments for a section/slide
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Section or slide ID
        comments: User comments
        
    Returns:
        Created refinement record with comments
    """
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
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
    
    # Get current content
    content = document.content or {}
    current_content = content.get(section_id, "")
    
    if not current_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Section/slide '{section_id}' has no content"
        )
    
    # Create refinement record with comments only (metadata)
    # TEMPORARY: Provide current content for frontend compatibility until migration is run
    refinement = Refinement(
        document_id=document.id,
        section_id=section_id,
        comments=comments,
        new_content=current_content  # TEMPORARY: Include current content for frontend
        # After migration, this field will be removed - content is stored in documents.content
    )
    
    db.add(refinement)
    db.commit()
    db.refresh(refinement)
    
    return refinement


def get_refinement_history(
    db: Session,
    project: Project,
    user: User,
    section_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Refinement]:
    """
    Get refinement history for a document or specific section/slide.
    Returns only metadata - content is in documents.content.
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Optional section/slide ID to filter by
        skip: Pagination offset
        limit: Pagination limit
        
    Returns:
        List of refinement records (metadata only)
    """
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
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
    
    # Query refinements (metadata only)
    query = db.query(Refinement).filter(Refinement.document_id == document.id)
    
    if section_id:
        query = query.filter(Refinement.section_id == section_id)
    
    refinements = query.order_by(
        Refinement.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return refinements


def get_feedback_for_sections(
    db: Session,
    project: Project,
    user: User,
    section_ids: Optional[List[str]] = None
) -> Dict[str, FeedbackType]:
    """
    Get feedback for sections from the Feedback table.
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_ids: Optional list of section IDs to filter by
        
    Returns:
        Dictionary mapping section_id to feedback_type
    """
    # Verify project belongs to user
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    # Get document
    document = get_document(db=db, project=project)
    if not document:
        return {}
    
    # Query feedback records
    query = db.query(Feedback).filter(Feedback.document_id == document.id)
    
    if section_ids:
        query = query.filter(Feedback.section_id.in_(section_ids))
    
    feedback_records = query.all()
    
    # Return as dictionary: {section_id: feedback_type}
    return {record.section_id: record.feedback_type for record in feedback_records}


def get_refinement_count(
    db: Session,
    project: Project,
    user: User,
    section_id: Optional[str] = None
) -> int:
    """
    Get total count of refinements
    
    Args:
        db: Database session
        project: Project object
        user: Authenticated user
        section_id: Optional section/slide ID to filter by
        
    Returns:
        Total count of refinements
    """
    # Verify project belongs to user (handle SQLite UUID strings)
    user_id_str = str(user.id) if isinstance(user.id, UUID) else user.id
    project_user_id_str = str(project.user_id) if isinstance(project.user_id, UUID) else project.user_id
    if project_user_id_str != user_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project does not belong to user"
        )
    
    # Get document
    document = get_document(db=db, project=project)
    if not document:
        return 0
    
    # Query count
    query = db.query(Refinement).filter(Refinement.document_id == document.id)
    
    if section_id:
        query = query.filter(Refinement.section_id == section_id)
    
    return query.count()

