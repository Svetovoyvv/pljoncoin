from models.user import User
from fastapi import Cookie, Depends, HTTPException, Header, Query
from models import SessionLocal
from sqlalchemy.orm import Session
from models.crud import UserCRUD
from cache import cache


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(token_cookie: str | None = Cookie(None, description='Токен авторизации', alias='token'),
             token_header: str | None = Header(None, description='Токен авторизации', alias='token'),
             token_query: str | None = Query(None, description='Токен авторизации', alias='token'),
             db: Session = Depends(get_db)) -> User | None:
    token = token_cookie or token_header or token_query
    if token is None:
        return None
    return UserCRUD.get_by_token(db, token)


def get_authorized(user: User | None = Depends(get_user)) -> User:
    if user is None:
        raise HTTPException(401, 'Unauthorized')
    return user

def admin_required(user: User = Depends(get_authorized)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Forbidden')
    return user

def get_crypt_course() -> tuple[float, float]:
    return cache.get('course')


def get_usd_course() -> float:
    return cache.get('usd')
