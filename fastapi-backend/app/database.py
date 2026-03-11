# 数据库连接、Session、init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# Create the asynchronous engine
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    future=True,
    pool_pre_ping=True
)

sessionmaker = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = engine
)

Base = declarative_base()

def get_db() -> Generator:
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

