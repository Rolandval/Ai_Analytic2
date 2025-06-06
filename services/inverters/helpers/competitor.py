from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import InvertersSuppliers

async def get_or_create_competitor(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:

    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    
    
    query = select(InvertersSuppliers).where(InvertersSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = InvertersSuppliers(name=suplier_name_upper, status_id=3)
    session.add(new_suplier)
    await session.flush()  
    return new_suplier.id

async def get_competitors_ids(session: AsyncSession = AsyncSession()):
    query = select(InvertersSuppliers).where(InvertersSuppliers.status_id == 3)
    result = await session.execute(query)
    return [suplier.id for suplier in result.scalars()]


async def get_competitors_name(func):
    if func.__name__ == "deye_ukraine":
        return "Deye Ukraine"

    