from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import User
from mysite.database.schema import UserSchema, UserCreateSchema
from mysite.api.auth import get_password_hash

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.post('/', response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        status=user.status
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/', response_model=List[UserSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get('/{user_id}', response_model=UserSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    return user_db


@user_router.put('/{user_id}', response_model=dict)
async def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    for key, value in user.model_dump().items():
        if key == 'password':
            value = get_password_hash(value)
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Updated'}


@user_router.patch('/{user_id}', response_model=dict)
async def partial_update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    for key, value in user.model_dump(exclude_unset=True).items():
        if key == 'password':
            value = get_password_hash(value)
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Partially Updated'}


@user_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(user_db)
    db.commit()
    return {'message': 'Deleted'}