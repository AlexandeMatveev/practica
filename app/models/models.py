from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base


class User(Base):
    """ORM-модель пользователя для PostgreSQL"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)


class Product(Base):
    """ORM-модель товара"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
