from models.user import User
from fastapi import Cookie, Depends, HTTPException
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


def get_authorized(token: str = Cookie(..., description='Токен авторизации'),
                   db: Session = Depends(get_db)) -> User:
    user = UserCRUD.get_by_token(db, token)
    if user is None:
        raise HTTPException(401, 'Unauthorized')
    return user


def get_user(token: str | None = Cookie(None, description='Токен авторизации'),
             db: Session = Depends(get_db)) -> User | None:
    if token is None:
        return None
    return UserCRUD.get_by_token(db, token)


def get_crypt_course() -> tuple[float, float]:
    return cache.get('course')


def get_usd_course() -> float:
    return cache.get('usd')
