from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, Boolean, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysite.database.db import Base


class StatusChoices(str, PyEnum):
    buyer = 'buyer'
    seller = 'seller'
    manager = 'manager'
    courier = 'courier'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.buyer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_review: Mapped[List['Review']] = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    user_order: Mapped[List['Order']] = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.username}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', back_populates='user_token')
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    category_store: Mapped[List['Store']] = relationship('Store', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.category_name}'


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(50), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='category_store')
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    store_product: Mapped[List['Product']] = relationship('Product', back_populates='store', cascade='all, delete-orphan')
    store_review: Mapped[List['Review']] = relationship('Review', back_populates='store', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.store_name}'


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_product')
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_original: Mapped[bool] = mapped_column(Boolean, default=True)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product_order: Mapped[List['Order']] = relationship('Order', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.product_name}'


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_review')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', back_populates='user_review')
    text: Mapped[str] = mapped_column(Text, nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.stars}'


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    city_order: Mapped[List['Order']] = relationship('Order', back_populates='city', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.city_name}'


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product', back_populates='product_order')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', back_populates='user_order')
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped['City'] = relationship('City', back_populates='city_order')
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.total_price}'