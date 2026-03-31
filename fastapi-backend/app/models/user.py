"""ORM model for the Users table (pga_platform.Users)."""
from sqlalchemy import Column, DateTime, Integer, String, func

from .base import Base


class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
