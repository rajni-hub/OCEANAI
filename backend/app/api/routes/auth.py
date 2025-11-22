"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_user_token
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    
    Returns the created user without password
    """
    try:
        user = create_user(db=db, user_create=user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login user and get access token
    
    - **username**: User email (OAuth2PasswordRequestForm uses 'username' field)
    - **password**: User password
    
    Returns JWT access token
    """
    # OAuth2PasswordRequestForm uses 'username' field for email
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = create_user_token(user=user)
    return token_data


@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user using JSON body (alternative to form-based login)
    
    - **email**: User email
    - **password**: User password
    
    Returns JWT access token
    """
    user = authenticate_user(db=db, email=login_data.email, password=login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = create_user_token(user=user)
    return token_data


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return current_user


@router.get("/verify-token")
async def verify_token(
    current_user: User = Depends(get_current_user)
):
    """
    Verify if the current JWT token is valid
    
    Returns success if token is valid
    """
    return {
        "valid": True,
        "user_id": str(current_user.id),
        "email": current_user.email
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresh the current user's access token
    
    Requires valid JWT token in Authorization header
    Returns a new access token
    """
    token_data = create_user_token(user=current_user)
    return token_data
