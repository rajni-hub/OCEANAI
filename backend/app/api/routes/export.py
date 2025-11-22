"""
Document export routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from io import BytesIO

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project, DocumentType
from app.services.project_service import get_project_by_id
from app.services.export_service import (
    export_word_document,
    export_powerpoint_document,
    get_export_filename
)

router = APIRouter()


@router.get(
    "/{project_id}/export",
    summary="Export document",
    description="Export finalized document as .docx (Word) or .pptx (PowerPoint) with latest refined content"
)
async def export_document(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export document as .docx or .pptx file
    
    - **project_id**: Project UUID
    - Returns downloadable file with latest refined content
    - File format depends on project document type
    
    The exported file includes:
    - All sections/slides from the document structure
    - Latest refined content for each section/slide
    - Proper formatting and structure preservation
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        # Export based on document type
        if project.document_type == DocumentType.WORD:
            file_stream = export_word_document(
                db=db,
                project=project,
                user=current_user
            )
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:  # powerpoint
            file_stream = export_powerpoint_document(
                db=db,
                project=project,
                user=current_user
            )
            media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        
        # Generate filename
        filename = get_export_filename(project)
        
        # Return as streaming response
        return StreamingResponse(
            file_stream,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting document: {str(e)}"
        )


@router.get(
    "/{project_id}/export/docx",
    summary="Export as Word document",
    description="Export document as .docx file (only for Word projects)"
)
async def export_word(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export Word document as .docx file
    
    - **project_id**: Project UUID
    - Returns downloadable .docx file
    - Only works for Word document projects
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        file_stream = export_word_document(
            db=db,
            project=project,
            user=current_user
        )
        
        filename = get_export_filename(project)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting Word document: {str(e)}"
        )


@router.get(
    "/{project_id}/export/pptx",
    summary="Export as PowerPoint document",
    description="Export document as .pptx file (only for PowerPoint projects)"
)
async def export_powerpoint(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export PowerPoint document as .pptx file
    
    - **project_id**: Project UUID
    - Returns downloadable .pptx file
    - Only works for PowerPoint document projects
    """
    # Verify project exists and belongs to user
    project = get_project_by_id(db=db, project_id=project_id, user=current_user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    try:
        file_stream = export_powerpoint_document(
            db=db,
            project=project,
            user=current_user
        )
        
        filename = get_export_filename(project)
        
        return StreamingResponse(
            file_stream,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting PowerPoint document: {str(e)}"
        )
