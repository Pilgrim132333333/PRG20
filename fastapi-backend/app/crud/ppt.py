from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ppt import PPT


#Input id
#Output PPT
async def get_ppt_by_id(db: AsyncSession, ppt_id: int):
    result = await db.execute(select(PPT).where(PPT.id == ppt_id))
    return result.scalar_one_or_none()

#Input unique_code
#Output PPT
async def get_ppt_by_unique_code(db: AsyncSession, unique_code: str):
    result = await db.execute(select(PPT).where(PPT.unique_code == unique_code))
    
    return result.scalar_one_or_none()

#Input id
#Output file_path
async def get_ppt_file_path_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(PPT.file_path).where(PPT.id == id))
    file_path = result.scalar_one_or_none()
    return  file_path

# Input: db, unique_code
# Output: True 删除成功，False 记录不存在
async def delete_ppt_by_unique_code(db: AsyncSession, unique_code: str) -> bool:
    ppt = await get_ppt_by_unique_code(db, unique_code)
    if not ppt:
        return False
    await db.delete(ppt)
    await db.flush()
    return True
