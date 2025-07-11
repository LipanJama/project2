from fastapi import APIRouter, Depends
from ..core.security import get_current_user, CurrentUser

router = APIRouter()

@router.get("/")
async def get_students(current_user: CurrentUser = Depends(get_current_user)):
    """Get students - placeholder"""
    return {"message": "Students endpoint - Coming soon"}