"""题库表 Model - 对应 pga_platform.Questions"""
from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from .base import Base


class Question(Base):
    __tablename__ = "Questions"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question_code = Column(String(50), unique=True, nullable=False)
    course_name = Column(String(100), default="Programming and Algorithms")
    source_year = Column(String(20), nullable=True)
    source_type = Column(
        Enum("Sample Paper", "CW", "Lab Worksheet", "Tutorial"),
        nullable=True,
    )
    knowledge_point = Column(String(512), nullable=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=True)
    language = Column(String(20), nullable=True)
