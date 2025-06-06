from sqlalchemy.ext.asyncio import AsyncSession
from db.models import SolarPanels, SolarPanelsPricesCurrent, SolarPanelsPrices
from sqlalchemy import select, update
from datetime import datetime


async def create_solar_panel(session: AsyncSession = AsyncSession(), solar_panel: dict = {}):
    try:
        new_solar_panel = SolarPanels(
            full_name=solar_panel['full_name'],
            power=solar_panel['power'],
            panel_type=solar_panel['panel_type'],
            cell_type=solar_panel['cell_type'],
            thickness=solar_panel['thickness'],
            brand_id=solar_panel['brand_id'],
            panel_color=solar_panel['panel_color'],
            frame_color=solar_panel['frame_color']
        )
        session.add(new_solar_panel)
        await session.flush()

        return new_solar_panel
    except Exception as e:
        print(e)


async def update_solar_panels_prices(session: AsyncSession = AsyncSession(), solar_panel: dict = {}):
    try:
        new_solar_panel_price = SolarPanelsPrices(
            price=solar_panel['price'],
            solar_panel_id=solar_panel['solar_panel_id'],
            supplier_id=solar_panel['supplier_id']
        )
        session.add(new_solar_panel_price)
        await session.flush()

        current = await session.execute(select(SolarPanelsPricesCurrent).where(SolarPanelsPricesCurrent.solar_panel_id == solar_panel['solar_panel_id'], SolarPanelsPricesCurrent.supplier_id == solar_panel['supplier_id']))
        if current.scalar_one_or_none():
            await session.execute(update(SolarPanelsPricesCurrent).where(SolarPanelsPricesCurrent.solar_panel_id == solar_panel['solar_panel_id'], SolarPanelsPricesCurrent.supplier_id == solar_panel['supplier_id']).values(price=solar_panel['price'], updated_at=datetime.now()))
        else:
            new_solar_panel_price_current = SolarPanelsPricesCurrent(
                price=solar_panel['price'],
                solar_panel_id=solar_panel['solar_panel_id'],
                supplier_id=solar_panel['supplier_id'],
                updated_at=datetime.now()
            )
            session.add(new_solar_panel_price_current)
            await session.flush()

        return "OK"

    except Exception as e:
        print(e)


async def delete_solar_panel(session: AsyncSession = AsyncSession(), solar_panel_id: int = 0):
    try:
        solar_panel = await session.execute(select(SolarPanels).where(SolarPanels.id == solar_panel_id))
        if solar_panel.scalar_one_or_none():
            await session.execute(delete(SolarPanels).where(SolarPanels.id == solar_panel_id))
            await session.flush()
            return "OK"
        else:
            return "Solar panel not found"
    except Exception as e:
        print(e)
    

async def get_all_solar_panels(session: AsyncSession = AsyncSession()):
    try:
        solar_panels_data = []
        solar_panels = await session.execute(select(SolarPanels))
        data = solar_panels.scalars().all()
        for solar_panel in data:
            solar_panels_data.append({
                "id": solar_panel.id,
                "full_name": solar_panel.full_name,
                "power": solar_panel.power,
                "panel_type": solar_panel.panel_type,
                "cell_type": solar_panel.cell_type,
                "thickness": solar_panel.thickness,
                "brand_id": solar_panel.brand_id,
                "brand": solar_panel.brand.name,
                "panel_color": solar_panel.panel_color,
                "frame_color": solar_panel.frame_color
            })
        return solar_panels_data
    except Exception as e:
        print(e)
    

    