from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta

from ..core.database import get_db, cache_manager
from ..core.security import (
    verify_password, get_password_hash, create_access_token, create_refresh_token,
    verify_token, get_current_user, CurrentUser, UserRole, get_tenant_from_subdomain
)
from ..models.user import User
from ..models.school import School


router = APIRouter()

# Pydantic models for requests/responses
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    school_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    role: UserRole = UserRole.ADMIN

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: dict
    school: dict


def get_user_by_email_and_school(db: Session, email: str, school_id: int) -> Optional[User]:
    """Get user by email within a specific school"""
    return db.query(User).filter(
        User.email == email,
        User.school_id == school_id,
        User.status == "active"
    ).first()


def get_school_by_subdomain(db: Session, subdomain: str) -> Optional[School]:
    """Get school by subdomain"""
    # Check cache first
    cache_key = f"school:subdomain:{subdomain}"
    cached_school = cache_manager.get(cache_key)
    
    if cached_school:
        # In a real implementation, you'd deserialize the cached data
        pass
    
    school = db.query(School).filter(
        School.subdomain == subdomain,
        School.subscription_status == "active"
    ).first()
    
    if school:
        # Cache the school data
        cache_manager.set(cache_key, str(school.id))
    
    return school


def authenticate_user(db: Session, email: str, password: str, school_id: int) -> Optional[User]:
    """Authenticate user credentials"""
    user = get_user_by_email_and_school(db, email, school_id)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login endpoint with multi-tenant support
    Extracts tenant from subdomain and authenticates user within that tenant
    """
    # Extract subdomain from request
    subdomain = await get_tenant_from_subdomain(request)
    
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomain is required for login"
        )
    
    # Get school by subdomain
    school = get_school_by_subdomain(db, subdomain)
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found or inactive"
        )
    
    # Authenticate user
    user = authenticate_user(db, user_credentials.email, user_credentials.password, school.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "school_id": school.id,
        "branch_id": user.branch_id
    }
    access_token = create_access_token(access_token_data, access_token_expires)
    
    # Create refresh token
    refresh_token = create_refresh_token(access_token_data)
    
    # Prepare user data for response
    user_data = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "role": user.role.value,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "branch_id": user.branch_id
    }
    
    # Prepare school data for response
    school_data = {
        "id": school.id,
        "name": school.name,
        "subdomain": school.subdomain,
        "logo_url": school.logo_url,
        "subscription_plan": school.subscription_plan.value
    }
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user_data,
        "school": school_data
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    # Verify refresh token
    payload = verify_token(token_request.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=30)
    access_token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "school_id": user.school_id,
        "branch_id": user.branch_id
    }
    access_token = create_access_token(access_token_data, access_token_expires)
    
    # Create new refresh token
    refresh_token = create_refresh_token(access_token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(current_user: CurrentUser = Depends(get_current_user)):
    """
    Logout endpoint
    In a real implementation, you would invalidate the token in Redis
    """
    # Add token to blacklist in Redis
    # cache_manager.set(f"blacklist:token:{token}", "1", expire=3600)
    
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user_info(current_user: CurrentUser = Depends(get_current_user)):
    """
    Get current user information
    """
    return {
        "id": current_user.user_id,
        "email": current_user.email,
        "role": current_user.role.value,
        "school_id": current_user.school_id,
        "branch_id": current_user.branch_id,
        "permissions": [p.value for p in current_user.permissions]
    }


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    # Get user from database
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    password_reset: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Initiate password reset process
    """
    # Extract subdomain
    subdomain = await get_tenant_from_subdomain(request)
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomain is required"
        )
    
    # Get school
    school = get_school_by_subdomain(db, subdomain)
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Check if user exists
    user = get_user_by_email_and_school(db, password_reset.email, school.id)
    
    # Always return success to prevent email enumeration
    # In a real implementation, send password reset email if user exists
    
    return {"message": "If the email exists, a password reset link has been sent"}


# Superadmin endpoints for user management
@router.post("/register-school-admin")
async def register_school_admin(
    user_data: UserRegister,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register a new school admin (Superadmin only)
    """
    if not current_user.is_superadmin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can register school admins"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        school_id=current_user.school_id,
        branch_id=current_user.branch_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role.value
    }