from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import InvertersBrands


async def get_or_create_brand(session: AsyncSession = AsyncSession(), brand_name: str = "") -> int:    
    if not brand_name:
        raise ValueError("Название бренда не может быть пустым")
    
    brand_name_upper = brand_name.strip().upper()
    
    query = select(InvertersBrands).where(InvertersBrands.name == brand_name_upper)
    result = await session.execute(query)
    brand = result.scalar_one_or_none()
    
    if brand:
        return brand.id
    
    new_brand = InvertersBrands(name=brand_name_upper)
    session.add(new_brand)
    await session.flush()
    return new_brand.id


async def get_brand_by_name(session: AsyncSession = AsyncSession(), brand_name: str = ""):
    if not brand_name:
        return None
    
    brand_name_upper = brand_name.strip().upper()
    
    query = select(InvertersBrands).where(InvertersBrands.name == brand_name_upper)
    result = await session.execute(query)
    return result.scalar_one_or_none()