from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.coursework import Coursework

#Input id
#Output Coursework
async def get_coursework_by_id(db: AsyncSession, coursework_id: int):
    result = await db.execute(select(Coursework).where(Coursework.id == coursework_id))
    return result.scalar_one_or_none()

#Input unique_code
#Output Coursework
async def get_coursework_by_unique_code(db: AsyncSession, unique_code: str):
    result = await db.execute(select(Coursework).where(Coursework.unique_code == unique_code))
    return result.scalar_one_or_none()


# Input: db, coursework_id
# Output: True 删除成功，False 记录不存在
async def delete_coursework_by_id(db: AsyncSession, coursework_id: int) -> bool:
    coursework = await get_coursework_by_id(db, coursework_id)
    if not coursework:
        return False
    await db.delete(coursework)
    await db.flush()
    return True


# Input: db, unique_code
# Output: True 删除成功，False 记录不存在
async def delete_coursework_by_unique_code(db: AsyncSession, unique_code: str) -> bool:
    coursework = await get_coursework_by_unique_code(db, unique_code)
    if not coursework:
        return False
    await db.delete(coursework)
    await db.flush()
    return True
