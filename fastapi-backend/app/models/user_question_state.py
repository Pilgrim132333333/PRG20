"""ORM model for the User_Question_State table (pga_platform.User_Question_State)."""
from sqlalchemy import Column, ForeignKey, Integer

from .base import Base


class UserQuestionState(Base):
    __tablename__ = "User_Question_State"

    user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="CASCADE"), primary_key=True)
    question_id = Column(Integer, ForeignKey("Questions.question_id", ondelete="CASCADE"), primary_key=True)
    is_favourite = Column(Integer, nullable=False, default=0)
    is_completed = Column(Integer, nullable=False, default=0)
