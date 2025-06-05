from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Batteries, BatteriesPricesCurrent, BatteriesPrices
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from datetime import datetime


async def create_battery(session: AsyncSession = AsyncSession(), battery: dict = {}):
    try:
        new_battery = Batteries(
            full_name=battery['full_name'],
            c_amps=battery['c_amps'],
            region=battery['region'],
            volume=battery['volume'],
            polarity=battery['polarity'],
            electrolyte=battery['electrolyte'],
            brand_id=battery['brand_id']
        )
        session.add(new_battery)
        await session.flush()

        return new_battery
    except Exception as e:
        print(e)


async def update_batteries_prices(session: AsyncSession = AsyncSession(), battery: dict = {}):
    try:
        # Додаємо запис в історію цін
        new_battery_price = BatteriesPrices(
            price=battery['price'],
            battery_id=battery['battery_id'],
            supplier_id=battery['supplier_id']
        )
        session.add(new_battery_price)
        await session.flush()

        # Перевіряємо, чи існує запис в поточних цінах
        stmt = select(BatteriesPricesCurrent).where(
            BatteriesPricesCurrent.battery_id == battery['battery_id'], 
            BatteriesPricesCurrent.supplier_id == battery['supplier_id']
        )
        result = await session.execute(stmt)
        current_price = result.scalar_one_or_none()

        # Якщо запис існує - оновлюємо ціну і дату
        if current_price:
            current_price.price = battery['price']
            current_price.updated_at = datetime.now()
            await session.flush()
        else:
            # Якщо запису немає - створюємо новий
            new_battery_price_current = BatteriesPricesCurrent(
                price=battery['price'],
                battery_id=battery['battery_id'],
                supplier_id=battery['supplier_id'],
                updated_at=datetime.now()
            )
            session.add(new_battery_price_current)
            await session.flush()

        return "OK"

    except Exception as e:
        print(e)


async def delete_battery(session: AsyncSession = AsyncSession(), battery_id: int = 0):
    try:
        battery = await session.execute(select(Batteries).where(Batteries.id == battery_id))
        if battery.scalar_one_or_none():
            await session.execute(delete(Batteries).where(Batteries.id == battery_id))
            await session.flush()
            await session.close()
            return "OK"
        else:
            await session.close()
            return "Battery not found"
    except Exception as e:
        print(e)


async def get_all_batteries(session: AsyncSession = AsyncSession()):
    try:
        batteries_data = []
        stmt = select(Batteries).options(joinedload(Batteries.brand))
        batteries = await session.execute(stmt)
        data = batteries.scalars().all()
        
        for battery in data:
            brand_name = None
            if battery.brand:
                brand_name = battery.brand.name
                
            batteries_data.append({
                "id": battery.id,
                "full_name": battery.full_name,
                "c_amps": battery.c_amps,
                "region": battery.region,
                "polarity": battery.polarity,
                "electrolyte": battery.electrolyte,
                "volume": battery.volume,
                "brand_id": battery.brand_id,
                "brand": brand_name
            })
        return batteries_data
    except Exception as e:
        print(e)
        return []