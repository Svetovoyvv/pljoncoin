from fastapi import APIRouter, Depends, HTTPException, Response
from models.user import UserRegister, UserPublic, UserAuthorized, UserLogin
from depends import get_db, Session
from models.crud import UserCRUD, AuthException
router = APIRouter(prefix='/auth', tags=['Authorization'])

@router.post('/register', response_model=UserPublic, responses={400: {'details': "User already exists"}})
async def register(
        user: UserRegister,
        db: Session = Depends(get_db)):
    user_db = UserCRUD.get_by_name(db, user.username) or UserCRUD.get_by_email(db, user.email)
    if user_db is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db = UserCRUD.register(db, user)
    return user_db

@router.post(
    '/login',
    response_model=UserAuthorized,
    responses={400: {'details': "Invalid username or password"}}
)
async def login(
        response: Response,
        user: UserLogin,
        db: Session = Depends(get_db)):
    try:
        user_db = UserCRUD.login(db, user)
    except AuthException:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    response.set_cookie(key='token', value=user_db.token)
    return user_db
