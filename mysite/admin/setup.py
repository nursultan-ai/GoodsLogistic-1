from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine
from mysite.admin.views import (
    UserAdmin, CategoryAdmin, StoreAdmin,
    ProductAdmin, ReviewAdmin, CityAdmin, OrderAdmin
)


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(OrderAdmin)