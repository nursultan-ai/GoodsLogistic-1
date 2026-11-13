from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from mysite.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIB, REFRESH_TOKEN_LIB
from mysite.database.db import get_db
from mysite.database.models import User, RefreshToken
from mysite.database.schema import UserCreateSchema, UserLoginSchema

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIB))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIB))


@auth_router.post('/register', response_model=dict)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(status_code=400, detail='Мындай username же email бар экен')

    hash_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password,
        status=user.status
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Регистрация ийгиликтүү болду'}


@auth_router.post('/login', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }


@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()
    return {'message': 'Вышли'}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': str(stored_token.id)})
    return {'access_token': access_token, 'token_type': 'Bearer'}