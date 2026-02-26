from fastapi import Depends, HTTPException, status
from src.auth.dependence import  get_current_user

async def admin_only(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create categories"
        )
    return user
