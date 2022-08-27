from fastapi import APIRouter, Depends, HTTPException
from depends import get_db, get_authorized
from models.user import User, UserPublic
from sqlalchemy.orm import Session
from models.crud import UserCRUD
router = APIRouter(prefix="/user", tags=['user'])

@router.get("/me", response_model=UserPublic)
async def profile(
        user: User = Depends(get_authorized)
):
    return user
@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    user = UserCRUD.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
