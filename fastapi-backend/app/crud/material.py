"""CRUD operations for the Materials table."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.material import Material


def get_material_by_id_sync(db: Session, material_id: int):
    result = db.execute(select(Material).where(Material.material_id == material_id))
    return result.scalar_one_or_none()


async def get_material_by_id(db: AsyncSession, material_id: int):
    result = await db.execute(select(Material).where(Material.material_id == material_id))
    return result.scalar_one_or_none()


async def get_material_by_code(db: AsyncSession, material_code: str):
    result = await db.execute(select(Material).where(Material.material_code == material_code))
    return result.scalar_one_or_none()


async def get_materials_all(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Material).offset(skip).limit(limit).order_by(Material.material_id)
    )
    return result.scalars().all()


async def delete_material(db: AsyncSession, material: Material):
    await db.delete(material)
    await db.flush()


async def delete_material_by_id(db: AsyncSession, material_id: int) -> bool:
    material = await get_material_by_id(db, material_id)
    if not material:
        return False
    await db.delete(material)
    await db.flush()
    return True


async def delete_material_by_code(db: AsyncSession, material_code: str) -> bool:
    material = await get_material_by_code(db, material_code)
    if not material:
        return False
    await db.delete(material)
    await db.flush()
    return True
