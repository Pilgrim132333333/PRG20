"""Question_Material_Link 表 CRUD"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question_material_link import QuestionMaterialLink
from app.models.material import Material


def get_materials_by_question_id(db: Session, question_id: int):
    """获取与题目关联的 Materials（同步）"""
    stmt = (
        select(Material)
        .join(QuestionMaterialLink, Material.material_id == QuestionMaterialLink.material_id)
        .where(QuestionMaterialLink.question_id == question_id)
    )
    result = db.execute(stmt)
    return result.scalars().all()


async def get_links_by_question_id(db: AsyncSession, question_id: int):
    result = await db.execute(
        select(QuestionMaterialLink).where(QuestionMaterialLink.question_id == question_id)
    )
    return result.scalars().all()


async def get_links_by_material_id(db: AsyncSession, material_id: int):
    result = await db.execute(
        select(QuestionMaterialLink).where(QuestionMaterialLink.material_id == material_id)
    )
    return result.scalars().all()


async def create_link(db: AsyncSession, question_id: int, material_id: int):
    link = QuestionMaterialLink(question_id=question_id, material_id=material_id)
    db.add(link)
    await db.flush()
    return link


async def delete_link(db: AsyncSession, link: QuestionMaterialLink):
    await db.delete(link)
    await db.flush()
