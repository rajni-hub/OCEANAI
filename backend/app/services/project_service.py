"""
Project service - Business logic for project management
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID
from app.models.project import Project, DocumentType
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    project_create: ProjectCreate,
    user: User
) -> Project:
    """
    Create a new project for the authenticated user
    
    Args:
        db: Database session
        project_create: Project creation data
        user: Authenticated user
        
    Returns:
        Created project object
        
    Raises:
        HTTPException: If validation fails
    """
    # Validate title
    if not project_create.title or len(project_create.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project title cannot be empty"
        )
    
    if len(project_create.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project title must be less than 255 characters"
        )
    
    # Validate main topic
    if not project_create.main_topic or len(project_create.main_topic.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Main topic cannot be empty"
        )
    
    if len(project_create.main_topic) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Main topic must be less than 500 characters"
        )
    
    # Create project
    db_project = Project(
        title=project_create.title.strip(),
        document_type=project_create.document_type,
        main_topic=project_create.main_topic.strip(),
        user_id=user.id
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


def get_project_by_id(
    db: Session,
    project_id: UUID,
    user: User
) -> Optional[Project]:
    """
    Get a project by ID, ensuring it belongs to the user
    
    Args:
        db: Database session
        project_id: Project UUID
        user: Authenticated user
        
    Returns:
        Project object if found and belongs to user, None otherwise
    """
    # For SQLite, IDs are stored as strings, so convert UUID to string for comparison
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        project_id_str = str(project_id)
        user_id_str = str(user.id)
        project = db.query(Project).filter(
            Project.id == project_id_str,
            Project.user_id == user_id_str
        ).first()
    else:
        # PostgreSQL uses UUID type
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user.id
        ).first()
    
    return project


def get_user_projects(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 100
) -> List[Project]:
    """
    Get all projects for a user with pagination
    
    Args:
        db: Database session
        user: Authenticated user
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Project objects
    """
    # For SQLite, user IDs are stored as strings
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        user_id_str = str(user.id)
        projects = db.query(Project).filter(
            Project.user_id == user_id_str
        ).order_by(
            Project.updated_at.desc()
        ).offset(skip).limit(limit).all()
    else:
        projects = db.query(Project).filter(
            Project.user_id == user.id
        ).order_by(
            Project.updated_at.desc()
        ).offset(skip).limit(limit).all()
    
    return projects


def update_project(
    db: Session,
    project_id: UUID,
    project_update: ProjectUpdate,
    user: User
) -> Project:
    """
    Update a project, ensuring it belongs to the user
    
    Args:
        db: Database session
        project_id: Project UUID
        project_update: Project update data
        user: Authenticated user
        
    Returns:
        Updated project object
        
    Raises:
        HTTPException: If project not found or doesn't belong to user
    """
    project = get_project_by_id(db=db, project_id=project_id, user=user)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields if provided
    update_data = project_update.model_dump(exclude_unset=True)
    
    if "title" in update_data:
        title = update_data["title"]
        if title is not None:
            title = title.strip()
            if len(title) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project title cannot be empty"
                )
            if len(title) > 255:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project title must be less than 255 characters"
                )
            project.title = title
    
    if "main_topic" in update_data:
        main_topic = update_data["main_topic"]
        if main_topic is not None:
            main_topic = main_topic.strip()
            if len(main_topic) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Main topic cannot be empty"
                )
            if len(main_topic) > 500:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Main topic must be less than 500 characters"
                )
            project.main_topic = main_topic
    
    db.commit()
    db.refresh(project)
    
    return project


def delete_project(
    db: Session,
    project_id: UUID,
    user: User
) -> bool:
    """
    Delete a project, ensuring it belongs to the user
    
    Args:
        db: Database session
        project_id: Project UUID
        user: Authenticated user
        
    Returns:
        True if deleted successfully
        
    Raises:
        HTTPException: If project not found or doesn't belong to user
    """
    project = get_project_by_id(db=db, project_id=project_id, user=user)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return True


def get_project_count(db: Session, user: User) -> int:
    """
    Get the total count of projects for a user
    
    Args:
        db: Database session
        user: Authenticated user
        
    Returns:
        Total number of projects
    """
    # For SQLite, user IDs are stored as strings
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        user_id_str = str(user.id)
        count = db.query(Project).filter(Project.user_id == user_id_str).count()
    else:
        count = db.query(Project).filter(Project.user_id == user.id).count()
    return count

