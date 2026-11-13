from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from mysite.database.models import StatusChoices


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    status: StatusChoices
    created_date: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    status: StatusChoices = StatusChoices.buyer


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    category_name: str


class StoreSchema(BaseModel):
    id: int
    store_name: str
    category_id: int
    store_image: Optional[str] = None

    class Config:
        from_attributes = True


class StoreCreateSchema(BaseModel):
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class ProductSchema(BaseModel):
    id: int
    store_id: int
    product_name: str
    price: float
    description: str
    is_original: bool
    create_date: datetime

    class Config:
        from_attributes = True


class ProductCreateSchema(BaseModel):
    store_id: int
    product_name: str
    price: float
    description: str
    is_original: bool = True


class ReviewSchema(BaseModel):
    id: int
    store_id: int
    user_id: int
    text: str
    stars: int = Field(..., ge=1, le=5)
    created_date: datetime

    class Config:
        from_attributes = True


class ReviewCreateSchema(BaseModel):
    store_id: int
    user_id: int
    text: str
    stars: int = Field(..., ge=1, le=5)


class CitySchema(BaseModel):
    id: int
    city_name: str

    class Config:
        from_attributes = True


class CityCreateSchema(BaseModel):
    city_name: str


class OrderSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    city_id: int
    quantity: int
    total_price: float
    created_date: datetime

    class Config:
        from_attributes = True


class OrderCreateSchema(BaseModel):
    product_id: int
    user_id: int
    city_id: int
    quantity: int = 1
    total_price: float