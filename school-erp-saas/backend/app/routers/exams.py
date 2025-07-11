from fastapi import APIRouter, Depends
from ..core.security import get_current_user, CurrentUser

router = APIRouter()

@router.get("/")
async def get_exams(current_user: CurrentUser = Depends(get_current_user)):
    """Get exams - placeholder"""
    return {"message": "Exams endpoint - Coming soon"}