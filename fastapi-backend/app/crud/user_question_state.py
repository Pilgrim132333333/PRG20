"""CRUD operations for the User_Question_State table."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_question_state import UserQuestionState


def get_state(db: Session, user_id: int, question_id: int) -> UserQuestionState | None:
    r = db.execute(
        select(UserQuestionState).where(
            UserQuestionState.user_id == user_id,
            UserQuestionState.question_id == question_id,
        )
    )
    return r.scalars().first()


def get_or_create_state(db: Session, user_id: int, question_id: int) -> UserQuestionState:
    row = get_state(db, user_id, question_id)
    if row:
        return row
    row = UserQuestionState(user_id=user_id, question_id=question_id, is_favourite=0, is_completed=0)
    db.add(row)
    db.flush()
    return row


def set_favourite(db: Session, user_id: int, question_id: int, value: int) -> None:
    row = get_or_create_state(db, user_id, question_id)
    row.is_favourite = 1 if value else 0
    db.commit()
    db.refresh(row)


def set_completed(db: Session, user_id: int, question_id: int, value: int) -> None:
    row = get_or_create_state(db, user_id, question_id)
    row.is_completed = 1 if value else 0
    db.commit()
    db.refresh(row)


def states_map_for_user(db: Session, user_id: int) -> dict[int, UserQuestionState]:
    r = db.execute(select(UserQuestionState).where(UserQuestionState.user_id == user_id))
    rows = r.scalars().all()
    return {x.question_id: x for x in rows}


def count_completed_for_user(db: Session, user_id: int) -> int:
    r = db.execute(
        select(UserQuestionState).where(
            UserQuestionState.user_id == user_id,
            UserQuestionState.is_completed == 1,
        )
    )
    return len(r.scalars().all())
