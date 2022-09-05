import datetime

import sqlalchemy as db
from sqlalchemy.orm import relationship
from . import Base
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    last_login = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String(256), nullable=False, unique=True)
    static_token = db.Column(db.String(256), nullable=False, unique=True)
    logs = relationship('LogEntry', back_populates='user')

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    register_date: datetime.datetime
    last_login: datetime.datetime
    is_admin: bool
    class Config:
        orm_mode = True

class UserAuthorized(BaseModel):
    username: str
    email: EmailStr
    token: str
    register_date: datetime.datetime
    is_admin: bool
    is_active: bool
    class Config:
        orm_mode = True

class UserPrivate(UserAuthorized):
    password: str
    class Config:
        orm_mode = True
