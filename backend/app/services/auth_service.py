"""
Authentication service - Business logic for user authentication
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.utils.validators import validate_email, validate_password_strength
from datetime import timedelta
from typing import Optional


def create_user(db: Session, user_create: UserCreate) -> User:
    """
    Create a new user with hashed password
    
    Args:
        db: Database session
        user_create: User creation data
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    # Validate email format
    if not validate_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Validate password strength
    if not validate_password_strength(user_create.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Get user by ID
    
    Args:
        db: Database session
        user_id: User UUID as string
        
    Returns:
        User object if found, None otherwise
    """
    from uuid import UUID
    try:
        uuid_obj = UUID(user_id)
        return db.query(User).filter(User.id == uuid_obj).first()
    except ValueError:
        return None


def create_user_token(user: User) -> dict:
    """
    Create JWT access token for user
    
    Args:
        user: User object
        
    Returns:
        Dictionary with access_token and token_type
    """
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
