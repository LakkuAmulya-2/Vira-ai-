from fastapi import APIRouter,Depends
from app.core.security import CurrentUser,get_current_user
router=APIRouter()
@router.get("/me")
async def me(user:CurrentUser=Depends(get_current_user)):
    return {"id":user.id,"role":user.role}
