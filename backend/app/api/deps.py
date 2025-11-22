"""
API dependencies for authentication and database sessions
"""
from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    
    This dependency is used to protect routes that require authentication.
    It validates the JWT token and returns the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    # For SQLite, user IDs are stored as strings, so query directly with string
    # For PostgreSQL, we would convert to UUID
    from app.core.config import settings
    if 'sqlite' in settings.DATABASE_URL.lower():
        # SQLite stores UUIDs as strings
        user = db.query(User).filter(User.id == user_id_str).first()
    else:
        # PostgreSQL uses UUID type
        try:
            user_id = UUID(user_id_str)
            user = db.query(User).filter(User.id == user_id).first()
        except (ValueError, TypeError):
            raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional dependency to get current user (returns None if not authenticated)
    """
    try:
        return get_current_user(token, db)
    except HTTPException:
        return None

