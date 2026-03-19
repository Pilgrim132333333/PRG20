"""物料表 Model - 对应 pga_platform.Materials"""
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .base import Base


class Material(Base):
    __tablename__ = "Materials"

    material_id = Column(Integer, primary_key=True, autoincrement=True)
    material_code = Column(String(50), unique=True, nullable=False)
    course_name = Column(String(100), default="Programming and Algorithms")
    material_type = Column(Enum("PPT", "Lab", "CW", "Tutorial"), nullable=False)
    week_number = Column(Integer, nullable=True)
    title = Column(String(200), nullable=True)
    file_path = Column(String(255), nullable=False)
