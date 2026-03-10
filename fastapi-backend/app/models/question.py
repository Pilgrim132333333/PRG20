#The data model for Question

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source_type = Column(String(50), nullable=False)
    ppt_id = Column(Integer, ForeignKey("ppt.id"))
    reated_at = Column(DateTime, default=datetime.now)
    unique_code = Column(String(50), nullable=False)
    ppt_unique_code = Column(String(50), nullable=True)
    answer_unique_code = Column(String(50), nullable=True)