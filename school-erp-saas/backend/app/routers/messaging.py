from fastapi import APIRouter, Depends
from ..core.security import get_current_user, CurrentUser

router = APIRouter()

@router.get("/")
async def get_messages(current_user: CurrentUser = Depends(get_current_user)):
    """Get messages - placeholder"""
    return {"message": "Messaging endpoint - Coming soon"}