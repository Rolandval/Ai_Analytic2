from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import BatteriesSuppliers

async def get_or_create_competitor(session: AsyncSession = AsyncSession(), suplier_name: str = "") -> int:

    if not suplier_name:
        raise ValueError("Название поставщика не может быть пустым")
    
    # Перетворюємо назву постачальника у верхній регістр
    suplier_name_upper = suplier_name.strip().upper()
    
    query = select(BatteriesSuppliers).where(BatteriesSuppliers.name == suplier_name_upper)
    result = await session.execute(query)
    suplier = result.scalar_one_or_none()
    
    if suplier:
        return suplier.id
    
    new_suplier = BatteriesSuppliers(name=suplier_name_upper, status_id=3)
    session.add(new_suplier)
    await session.flush()  
    return new_suplier.id

async def get_competitors_ids(session: AsyncSession = AsyncSession()):
    query = select(BatteriesSuppliers).where(BatteriesSuppliers.status_id == 3)
    result = await session.execute(query)
    return [suplier.id for suplier in result.scalars()]


async def get_competitors_name(func):
    if func.__name__ == "parse_batteries_avto_zvuk":  
        return "Авто Звук"
    if func.__name__ == "parse_batteries_aku_lviv":  
        return "Акумулятори Львів (aku.lviv)"
    if func.__name__ == "parse_batteries_makb":  
        return "MAKB"
    if func.__name__ == "parse_batteries_shyp_shuna":  
        return "Shyp-Shyna"
    if func.__name__ == "parse_batteries_aet_ua":  
        return "AET UA"
    if func.__name__ == "parse_batteries_akb_mag":  
        return "AKB Mag"
    if func.__name__ == "parse_batteries_akb_plus":  
        return "AKB Plus"
    if func.__name__ == "parse_batteries_dvi_klemy":  
        return "DVI Klemy"

    