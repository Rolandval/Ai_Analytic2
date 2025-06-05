from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import InvertersSuppliers

async def get_or_create_supplier(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:
    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    suplier_name_upper = suplier_name.strip().upper()
    
    query = select(InvertersSuppliers).where(InvertersSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = InvertersSuppliers(name=suplier_name_upper, is_me=False, is_supplier=True, is_competitor=False)
    session.add(new_suplier)
    await session.flush()  
    
    return new_suplier.id