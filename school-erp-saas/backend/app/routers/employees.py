from fastapi import APIRouter, Depends
from ..core.security import get_current_user, CurrentUser

router = APIRouter()

@router.get("/")
async def get_employees(current_user: CurrentUser = Depends(get_current_user)):
    """Get employees - placeholder"""
    return {"message": "Employees endpoint - Coming soon"}