"""Questions 表 CRUD"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.user_question_state import UserQuestionState


def get_question_by_id_sync(db: Session, question_id: int) -> Question | None:
    r = db.execute(select(Question).where(Question.question_id == question_id))
    return r.scalars().first()


def get_questions_by_ids(db: Session, question_ids: list[int]) -> list:
    """按 ID 列表获取题目，保持传入顺序"""
    if not question_ids:
        return []
    result = db.execute(
        select(Question).where(Question.question_id.in_(question_ids))
    )
    rows = result.scalars().all()
    order_map = {qid: i for i, qid in enumerate(question_ids)}
    return sorted(rows, key=lambda q: order_map.get(q.question_id, 999))


def get_questions_all(
    db: Session,
    skip: int = 0,
    limit: int = 10000,
    user_id: int | None = None,
    favourite: int | None = None,
):
    """获取所有题目；favourite=1 时需 user_id，按 User_Question_State.is_favourite 筛选"""
    stmt = select(Question)
    if user_id is not None and favourite == 1:
        stmt = (
            stmt.join(UserQuestionState, Question.question_id == UserQuestionState.question_id)
            .where(UserQuestionState.user_id == user_id)
            .where(UserQuestionState.is_favourite == 1)
        )
    elif favourite == 1:
        # 无 user_id 时无法按收藏筛选，返回空
        return []
    stmt = stmt.order_by(Question.question_id).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()


async def get_question_by_id(db, question_id: int):
    result = await db.execute(select(Question).where(Question.question_id == question_id))
    return result.scalar_one_or_none()


async def get_question_by_code(db, question_code: str):
    result = await db.execute(select(Question).where(Question.question_code == question_code))
    return result.scalar_one_or_none()


async def delete_question(db, question: Question):
    await db.delete(question)
    await db.flush()


async def delete_question_by_id(db, question_id: int) -> bool:
    question = await get_question_by_id(db, question_id)
    if not question:
        return False
    await db.delete(question)
    await db.flush()
    return True


async def delete_question_by_code(db, question_code: str) -> bool:
    question = await get_question_by_code(db, question_code)
    if not question:
        return False
    await db.delete(question)
    await db.flush()
    return True

def select_all_coursework(db, skip: int = 0, limit: int = 100) -> list:
    """从 Questions 表中选取 source_type='CW' 的题目作为 coursework"""
    result = db.execute(
        select(Question)
        .where(Question.source_type == "CW")
        .offset(skip)
        .limit(limit)
        .order_by(Question.question_id)
    )
    return result.scalars().all()