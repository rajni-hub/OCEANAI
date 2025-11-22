"""
Project management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse
)
from app.services.project_service import (
    create_project,
    get_project_by_id,
    get_user_projects,
    update_project,
    delete_project,
    get_project_count
)

router = APIRouter()


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new document project for the authenticated user"
)
async def create_new_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new project
    
    - **title**: Project title (1-255 characters)
    - **document_type**: Document type (word or powerpoint)
    - **main_topic**: Main topic or prompt (1-500 characters)
    
    Returns the created project
    """
    try:
        project = create_project(
            db=db,
            project_create=project_data,
            user=current_user
        )
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating project: {str(e)}"
        )


@router.get(
    "",
    response_model=ProjectListResponse,
    summary="List user's projects",
    description="Get all projects belonging to the authenticated user with pagination"
)
async def list_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all projects for the authenticated user
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return (pagination limit)
    
    Returns a list of projects with pagination info
    """
    try:
        projects = get_user_projects(
            db=db,
            user=current_user,
            skip=skip,
            limit=limit
        )
        total = get_project_count(db=db, user=current_user)
        
        return ProjectListResponse(
            projects=projects,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching projects: {str(e)}"
        )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Get a specific project by ID (must belong to authenticated user)"
)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a project by ID
    
    - **project_id**: Project UUID
    
    Returns the project if it belongs to the authenticated user
    """
    project = get_project_by_id(
        db=db,
        project_id=project_id,
        user=current_user
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="Update a project (must belong to authenticated user)"
)
async def update_existing_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a project
    
    - **project_id**: Project UUID
    - **title**: New project title (optional)
    - **main_topic**: New main topic (optional)
    
    Returns the updated project
    """
    try:
        project = update_project(
            db=db,
            project_id=project_id,
            project_update=project_update,
            user=current_user
        )
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating project: {str(e)}"
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description="Delete a project (must belong to authenticated user)"
)
async def delete_existing_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a project
    
    - **project_id**: Project UUID
    
    Returns 204 No Content on success
    """
    try:
        delete_project(
            db=db,
            project_id=project_id,
            user=current_user
        )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting project: {str(e)}"
        )


@router.get(
    "/{project_id}/exists",
    summary="Check if project exists",
    description="Check if a project exists and belongs to the authenticated user"
)
async def check_project_exists(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if a project exists and belongs to the user
    
    - **project_id**: Project UUID
    
    Returns existence status
    """
    project = get_project_by_id(
        db=db,
        project_id=project_id,
        user=current_user
    )
    
    return {
        "exists": project is not None,
        "project_id": str(project_id)
    }
