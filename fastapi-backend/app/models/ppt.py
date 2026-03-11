#data model for ppt

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class PPT(Base):
    __tablename__ = "ppt"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(255),nullable=False)
    description = Column(Text, nullable=True)
    uoloaded_at = Column(DateTime, default=datetime.now)
    course_name = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    unique_code = Column(String(50), nullable=False)