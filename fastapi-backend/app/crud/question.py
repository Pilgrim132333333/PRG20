from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question

#Input id
#Output Question
async def get_question_by_id(db: AsyncSession, question_id: int):
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()

#Input unique_code
#Output Question
async def get_question_by_unique_code(db: AsyncSession, unique_code: str):
    result = await db.execute(select(Question).where(Question.unique_code == unique_code))
    return result.scalar_one_or_none()


# Input: db, question_id
# Output: True 删除成功，False 记录不存在
async def delete_question_by_id(db: AsyncSession, question_id: int) -> bool:
    question = await get_question_by_id(db, question_id)
    if not question:
        return False
    await db.delete(question)
    await db.flush()
    return True


# Input: db, unique_code
# Output: True 删除成功，False 记录不存在
async def delete_question_by_unique_code(db: AsyncSession, unique_code: str) -> bool:
    question = await get_question_by_unique_code(db, unique_code)
    if not question:
        return False
    await db.delete(question)
    await db.flush()
    return True