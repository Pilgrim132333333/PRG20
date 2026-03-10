from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.answer import Answer

#Input id
#Output Answer
async def get_answer_by_id(db: AsyncSession, answer_id: int):
    result = await db.execute(select(Answer).where(Answer.id == answer_id))
    return result.scalar_one_or_none()

#Input unique_code
#Output Answer
async def get_answer_by_unique_code(db: AsyncSession, unique_code: str):
    result = await db.execute(select(Answer).where(Answer.unique_code == unique_code))
    return result.scalar_one_or_none()


# Input: db, answer_id
# Output: True 删除成功，False 记录不存在
async def delete_answer_by_id(db: AsyncSession, answer_id: int) -> bool:
    answer = await get_answer_by_id(db, answer_id)
    if not answer:
        return False
    await db.delete(answer)
    await db.flush()
    return True


# Input: db, unique_code
# Output: True 删除成功，False 记录不存在
async def delete_answer_by_unique_code(db: AsyncSession, unique_code: str) -> bool:
    answer = await get_answer_by_unique_code(db, unique_code)
    if not answer:
        return False
    await db.delete(answer)
    await db.flush()
    return True
