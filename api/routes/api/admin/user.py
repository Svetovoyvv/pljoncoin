from fastapi import APIRouter, Depends
from models.crud import UserCRUD
from models.user import UserPublic
from depends import get_db, Session
router = APIRouter(prefix='/user', tags=['User'])

@router.get('/all', response_model=list[UserPublic], summary='Получение всех пользователей')
async def get_all(db: Session = Depends(get_db)) -> list[UserPublic]:
    return UserCRUD.get_all(db)



