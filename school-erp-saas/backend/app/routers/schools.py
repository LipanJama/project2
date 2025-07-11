from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

from ..core.database import get_db
from ..core.security import get_current_user, CurrentUser, require_superadmin
from ..models.school import School, Branch, SubscriptionPlan, SubscriptionStatus

router = APIRouter()

# Pydantic models
class SchoolCreate(BaseModel):
    name: str
    subdomain: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.BASIC
    monthly_fee: float = 0.00

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    subscription_plan: Optional[SubscriptionPlan] = None
    subscription_status: Optional[SubscriptionStatus] = None
    monthly_fee: Optional[float] = None

class SchoolResponse(BaseModel):
    id: int
    name: str
    subdomain: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    subscription_plan: str
    subscription_status: str
    monthly_fee: float
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[SchoolResponse])
async def get_schools(
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = Depends(require_superadmin()),
    db: Session = Depends(get_db)
):
    """Get all schools (Superadmin only)"""
    schools = db.query(School).offset(skip).limit(limit).all()
    return schools

@router.post("/", response_model=SchoolResponse)
async def create_school(
    school_data: SchoolCreate,
    current_user: CurrentUser = Depends(require_superadmin()),
    db: Session = Depends(get_db)
):
    """Create a new school (Superadmin only)"""
    # Check if subdomain already exists
    existing_school = db.query(School).filter(School.subdomain == school_data.subdomain).first()
    if existing_school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomain already exists"
        )
    
    school = School(**school_data.dict())
    db.add(school)
    db.commit()
    db.refresh(school)
    
    return school

@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get school by ID"""
    # Superadmin can access any school, others only their own
    if not current_user.is_superadmin() and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    return school

@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    current_user: CurrentUser = Depends(require_superadmin()),
    db: Session = Depends(get_db)
):
    """Update school (Superadmin only)"""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    for field, value in school_data.dict(exclude_unset=True).items():
        setattr(school, field, value)
    
    db.commit()
    db.refresh(school)
    
    return school

@router.delete("/{school_id}")
async def delete_school(
    school_id: int,
    current_user: CurrentUser = Depends(require_superadmin()),
    db: Session = Depends(get_db)
):
    """Delete school (Superadmin only)"""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    db.delete(school)
    db.commit()
    
    return {"message": "School deleted successfully"}