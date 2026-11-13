from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Order
from mysite.database.schema import OrderSchema, OrderCreateSchema

order_router = APIRouter(prefix='/order', tags=['Order'])


@order_router.post('/', response_model=OrderSchema)
async def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.model_dump())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get('/', response_model=List[OrderSchema])
async def list_order(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}', response_model=OrderSchema)
async def detail_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(status_code=404, detail='Order not found')
    return order_db


@order_router.put('/{order_id}', response_model=dict)
async def update_order(order_id: int, order: OrderCreateSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(status_code=404, detail='Order not found')

    for key, value in order.model_dump().items():
        setattr(order_db, key, value)

    db.commit()
    db.refresh(order_db)
    return {'message': 'Updated'}


@order_router.delete('/{order_id}', response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(status_code=404, detail='Order not found')

    db.delete(order_db)
    db.commit()
    return {'message': 'Deleted'}