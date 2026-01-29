from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, UserUpdate
from app.services.auth_service import AuthService
from app.models.user import UserRole
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = AuthService.register_user(db, user, UserRole.USER)
        return {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "role": db_user.role,
            "full_name": db_user.full_name,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_admin(user: UserCreate, db = Depends(get_db)):
    """Register a new admin"""
    try:
        db_user = AuthService.register_user(db, user, UserRole.ADMIN)
        return {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "role": db_user.role,
            "full_name": db_user.full_name,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(email: str, password: str, db = Depends(get_db)):
    """Login user"""
    user = AuthService.authenticate_user(db, email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = AuthService.create_access_token_for_user(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }


@router.put("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update current user"""
    updated_user = AuthService.update_user(db, current_user, user_update)
    return {
        "id": updated_user.id,
        "email": updated_user.email,
        "username": updated_user.username,
        "role": updated_user.role,
        "full_name": updated_user.full_name,
        "is_active": updated_user.is_active,
        "created_at": updated_user.created_at,
        "updated_at": updated_user.updated_at
    }
