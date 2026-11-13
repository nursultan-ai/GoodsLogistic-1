from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Store
from mysite.database.schema import StoreSchema, StoreCreateSchema

store_router = APIRouter(prefix='/store', tags=['Store'])


@store_router.post('/', response_model=StoreSchema)
async def create_store(store: StoreCreateSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.model_dump())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/', response_model=List[StoreSchema])
async def list_store(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store_id}', response_model=StoreSchema)
async def detail_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail='Store not found')
    return store_db


@store_router.put('/{store_id}', response_model=dict)
async def update_store(store_id: int, store: StoreCreateSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail='Store not found')

    for key, value in store.model_dump().items():
        setattr(store_db, key, value)

    db.commit()
    db.refresh(store_db)
    return {'message': 'Updated'}


@store_router.patch('/{store_id}', response_model=dict)
async def partial_update_store(store_id: int, store: StoreCreateSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail='Store not found')

    for key, value in store.model_dump(exclude_unset=True).items():
        setattr(store_db, key, value)

    db.commit()
    db.refresh(store_db)
    return {'message': 'Partially Updated'}


@store_router.delete('/{store_id}', response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(status_code=404, detail='Store not found')

    db.delete(store_db)
    db.commit()
    return {'message': 'Deleted'}