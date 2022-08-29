from .user import User, UserRegister, UserLogin, UserAuthorized
from sqlalchemy.orm import Session
from hashlib import sha256
import datetime
import os
class AuthException(Exception):
    pass
class UserCRUD:
    __slots__ = ()
    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
    @classmethod
    def get_by_name(cls, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()
    @classmethod
    def get_by_email(cls, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    @classmethod
    def get_by_token(cls, db: Session, token: str) -> User | None:
        user = db.query(User).filter((User.token == token) | (User.static_token == token)).first()
        if user is None:
            return None
        if user.is_active and user.last_login > datetime.datetime.now() - datetime.timedelta(days=1):
            return user

    @classmethod
    def get_all(cls, db: Session) -> list[User]:
        return db.query(User).all()
    @classmethod
    def create(cls, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    @classmethod
    def register(cls, db: Session, user: UserRegister) -> User:
        user.password = cls.Security.hash_password(user.password)
        muser = User(
            username=user.username,
            email=user.email,
            password=user.password,
            register_date=datetime.datetime.now(),
            is_active=True,
            is_admin=False,
            token=user.password + user.email,
            static_token=user.password + user.email + 'static'
        )
        muser = cls.create(db, muser)
        muser.static_token = cls.Security.generate_token(muser.id)
        db.commit()
        return muser
    @classmethod
    def login(cls, db: Session, user: UserLogin) -> User:
        user_db = cls.get_by_email(db, user.email)
        if user_db is None:
            raise AuthException('User not found')
        if not cls.Security.check_password(user_db.password, user.password):
            raise AuthException('Invalid password')
        user_db.last_login = datetime.datetime.now()
        user_db.token = cls.Security.generate_token(user_db.id)
        db.commit()
        return user_db
    class Security:
        @classmethod
        def random_salt(cls, length: int = 16) -> str:
            return os.urandom(length).hex()
        @classmethod
        def hash_password(cls, password: str, salt: str | None = None) -> str:
            salt = salt or cls.random_salt()
            return '{}${}'.format(
                salt,
                sha256((password + salt).encode('utf-8')).hexdigest()
            )
        @classmethod
        def check_password(cls, hashed_password: str, password: str) -> bool:
            salt, _ = hashed_password.split('$')
            return hashed_password == cls.hash_password(password, salt)
        @classmethod
        def generate_token(cls, user_id: int) -> str:
            return '{}:{}'.format(user_id, cls.random_salt(96))