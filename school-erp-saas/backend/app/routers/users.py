from fastapi import APIRouter
from ..core.security import get_current_user, CurrentUser
from fastapi import Depends

router = APIRouter()

@router.get("/")
async def get_users(current_user: CurrentUser = Depends(get_current_user)):
    """Get users - placeholder"""
    return {"message": "Users endpoint - Coming soon"}

@router.post("/")
async def create_user(current_user: CurrentUser = Depends(get_current_user)):
    """Create user - placeholder"""
    return {"message": "Create user endpoint - Coming soon"}