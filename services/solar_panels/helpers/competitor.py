from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import SolarPanelsSuppliers

async def get_or_create_competitor(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:

    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    
    
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = SolarPanelsSuppliers(name=suplier_name_upper, is_me=False, is_supplier=False, is_competitor=True)
    session.add(new_suplier)
    await session.flush()  
    return new_suplier.id

async def get_competitors_ids(session: AsyncSession = AsyncSession()):
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.is_competitor == True)
    result = await session.execute(query)
    return [suplier.id for suplier in result.scalars()]


async def get_competitors_name(func):
    ...

    