from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import SolarPanelsSuppliers

async def get_or_create_competitor(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:

    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    suplier_name_upper = suplier_name.upper()
    
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = SolarPanelsSuppliers(name=suplier_name_upper, status_id=3)
    session.add(new_suplier)
    await session.flush()  
    return new_suplier.id

async def get_competitors_ids(session: AsyncSession = AsyncSession()):
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.status_id == 3)
    result = await session.execute(query)
    return [suplier.id for suplier in result.scalars()]


async def get_competitors_name(func):
    if func.__name__ == "parse_solar_panels_solarflow":  
        return "Solarflow"
    if func.__name__ == "parse_solar_panels_friends_solar":  
        return "Friends Solar"
    