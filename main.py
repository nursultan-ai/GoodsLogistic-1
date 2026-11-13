import uvicorn
from fastapi import FastAPI
from mysite.database.db import engine, Base
from mysite.admin.setup import setup_admin
from mysite.api import auth, user, category, store, product, review, city, order

Base.metadata.create_all(bind=engine)

shop_app = FastAPI(title='GoodsLogistic-Nurs')

setup_admin(shop_app)

shop_app.include_router(auth.auth_router)
shop_app.include_router(user.user_router)
shop_app.include_router(category.category_router)
shop_app.include_router(store.store_router)
shop_app.include_router(product.product_router)
shop_app.include_router(review.review_router)
shop_app.include_router(city.city_router)
shop_app.include_router(order.order_router)

if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=8000)