from fastapi import APIRouter, Depends
from ..core.security import get_current_user, CurrentUser

router = APIRouter()

@router.get("/")
async def get_payroll(current_user: CurrentUser = Depends(get_current_user)):
    """Get payroll - placeholder"""
    return {"message": "Payroll endpoint - Coming soon"}