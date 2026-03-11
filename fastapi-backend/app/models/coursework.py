#The model for Coursework

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Coursework(Base):
    __tablename__ = "courseworks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(255),nullable=False)
    description = Column(Text, nullable=True)
    unique_code = Column(String(50), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now)
    ppt_unique_code = Column(String(50), nullable=True)