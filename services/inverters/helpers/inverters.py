from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Inverters, InvertersPricesCurrent, InvertersPrices
from sqlalchemy import select, update
from datetime import datetime


async def create_inverter(session: AsyncSession = AsyncSession(), inverter: dict = {}):
    try:
        new_inverter = Inverters(
            full_name=inverter['full_name'],
            power=inverter['power'],
            inverter_type=inverter['inverter_type'],
            generation=inverter['generation'],
            string_count=inverter['string_count'],
            brand_id=inverter['brand_id'],
            firmware=inverter['firmware']
        )
        session.add(new_inverter)
        await session.flush()

        return new_inverter
    except Exception as e:
        print(e)


async def update_inverters_prices(session: AsyncSession = AsyncSession(), inverter: dict = {}):
    try:
        new_inverter_price = InvertersPrices(
            price=inverter['price'],
            inverter_id=inverter['inverter_id'],
            supplier_id=inverter['supplier_id']
        )
        session.add(new_inverter_price)
        await session.flush()

        current = await session.execute(select(InvertersPricesCurrent).where(InvertersPricesCurrent.inverter_id == inverter['inverter_id'], InvertersPricesCurrent.supplier_id == inverter['supplier_id']))
        if current.scalar_one_or_none():
            await session.execute(update(InvertersPricesCurrent).where(InvertersPricesCurrent.inverter_id == inverter['inverter_id'], InvertersPricesCurrent.supplier_id == inverter['supplier_id']).values(price=inverter['price'], updated_at=datetime.now()))
        else:
            new_inverter_price_current = InvertersPricesCurrent(
                price=inverter['price'],
                inverter_id=inverter['inverter_id'],
                supplier_id=inverter['supplier_id'],
                updated_at=datetime.now()
            )
            session.add(new_inverter_price_current)
            await session.flush()

        return "OK"

    except Exception as e:
        print(e)


async def delete_inverter(session: AsyncSession = AsyncSession(), inverter_id: int = 0):
    try:
        inverter = await session.execute(select(Inverters).where(Inverters.id == inverter_id))
        if inverter.scalar_one_or_none():
            await session.execute(delete(Inverters).where(Inverters.id == inverter_id))
            await session.flush()
            return "OK"
        else:
            return "Inverter not found"
    except Exception as e:
        print(e)
    

async def get_all_inverters(session: AsyncSession = AsyncSession()):
    try:
        inverters_data = []
        inverters = await session.execute(select(Inverters))
        data = inverters.scalars().all()
        for inverter in data:
            inverters_data.append({
                "id": inverter.id,
                "full_name": inverter.full_name,
                "power": inverter.power,
                "inverter_type": inverter.inverter_type,
                "generation": inverter.generation,
                "string_count": inverter.string_count,
                "brand_id": inverter.brand_id,
                "brand": inverter.brand.name
            })
        return inverters_data
    except Exception as e:
        print(e)
    

    