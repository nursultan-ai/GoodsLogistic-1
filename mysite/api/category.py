from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Category
from mysite.database.schema import CategorySchema, CategoryCreateSchema

category_router = APIRouter(prefix='/category', tags=['Category'])


@category_router.post('/', response_model=CategorySchema)
async def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.model_dump())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get('/', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}', response_model=CategorySchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')
    return category_db


@category_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: CategoryCreateSchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    for key, value in category.model_dump().items():
        setattr(category_db, key, value)

    db.commit()
    db.refresh(category_db)
    return {'message': 'Updated'}


@category_router.delete('/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'Deleted'} 