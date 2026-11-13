from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import City
from mysite.database.schema import CitySchema, CityCreateSchema

city_router = APIRouter(prefix='/city', tags=['City'])


@city_router.post('/', response_model=CitySchema)
async def create_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    city_db = City(**city.model_dump())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.get('/', response_model=List[CitySchema])
async def list_city(db: Session = Depends(get_db)):
    return db.query(City).all()


@city_router.get('/{city_id}', response_model=CitySchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail='City not found')
    return city_db


@city_router.put('/{city_id}', response_model=dict)
async def update_city(city_id: int, city: CityCreateSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail='City not found')

    for key, value in city.model_dump().items():
        setattr(city_db, key, value)

    db.commit()
    db.refresh(city_db)
    return {'message': 'Updated'}


@city_router.delete('/{city_id}', response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(status_code=404, detail='City not found')

    db.delete(city_db)
    db.commit()
    return {'message': 'Deleted'}