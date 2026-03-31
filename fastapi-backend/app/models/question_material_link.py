"""ORM model for pga_platform.Question_Material_Link (many-to-many join table)."""
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint

from .base import Base


class QuestionMaterialLink(Base):
    __tablename__ = "Question_Material_Link"

    question_id = Column(Integer, ForeignKey("Questions.question_id", ondelete="CASCADE"), primary_key=True)
    material_id = Column(Integer, ForeignKey("Materials.material_id", ondelete="CASCADE"), primary_key=True)
