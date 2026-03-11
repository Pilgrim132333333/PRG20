# The data model of Answer

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    content = Column(Text, nullable=False)
    file_path = Column(String(255),nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    unique_code = Column(String(50), nullable=False)
    question_unique_code = Column(String(50), nullable=False)

