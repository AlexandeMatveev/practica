from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    """ORM-модель пользователя для PostgreSQL"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)