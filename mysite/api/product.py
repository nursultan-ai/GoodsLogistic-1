from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Product
from mysite.database.schema import ProductSchema, ProductCreateSchema

product_router = APIRouter(prefix='/product', tags=['Product'])


@product_router.post('/', response_model=ProductSchema)
async def create_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}', response_model=ProductSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')
    return product_db


@product_router.put('/{product_id}', response_model=dict)
async def update_product(product_id: int, product: ProductCreateSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    for key, value in product.model_dump().items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Updated'}


@product_router.patch('/{product_id}', response_model=dict)
async def partial_update_product(product_id: int, product: ProductCreateSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Partially Updated'}


@product_router.delete('/{product_id}', response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product_db)
    db.commit()
    return {'message': 'Deleted'}