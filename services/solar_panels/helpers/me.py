from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import SolarPanelsSuppliers

async def get_or_create_me(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:

    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    suplier_name_upper = suplier_name.strip().upper()
    
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = SolarPanelsSuppliers(name=suplier_name_upper, status_id=1)
    session.add(new_suplier)
    await session.flush()  
    return new_suplier.id

async def get_my_id(session: AsyncSession = AsyncSession()) -> int:
    query = select(SolarPanelsSuppliers).where(SolarPanelsSuppliers.status_id == 1)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    raise ValueError("Не зареєстрований")