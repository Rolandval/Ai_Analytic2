from services.solar_panels.helpers.supplier import get_or_create_supplier
from services.solar_panels.helpers.me import get_or_create_me
from services.solar_panels.helpers.competitor import get_or_create_competitor
from services.solar_panels.helpers.solar_panels import update_solar_panels_prices
from services.solar_panels.helpers.brand import get_or_create_brand
from services.solar_panels.helpers.solar_panels import create_solar_panel
from services.solar_panels.backend.schemas import SolarPanelCreateSchema
from prompts.solar_panels.get_prices_prompt import get_prices_prompt
from prompts.solar_panels.add_new_solar_panel_prompt import add_new_prompt
from filters.solar_panels_filter import ai_filter
from helpers.ai_req import gemini_request   
from db.database import get_session

async def import_data(data, supplier_name, supplier_type):
    # Отримуємо сесію бази даних
    async with get_session() as session:
        supplier_func = None
        if supplier_type == "me":
            supplier_func = get_or_create_me
        if supplier_type == "supplier":
            supplier_func = get_or_create_supplier
        if supplier_type == "competitor":
            supplier_func = get_or_create_competitor

        filter_data = ai_filter(data)
        lenth = len(filter_data)
        chunk_size = 45
        all_data = []
        
        for i in range(0, lenth, chunk_size):
            chunk = filter_data[i:i + chunk_size]
            prompt = await get_prices_prompt(data=chunk, session=session)
            result = await gemini_request(prompt)
            print(f"result: {result}")
            # Перевіряємо, чи result є списком
            if isinstance(result, list):
                all_data.extend(result)  # Додаємо елементи списку до all_data
            else:
                all_data.append(result)  # Додаємо один елемент
        
        # Передаємо сесію в функцію supplier_func
        supplier_id = await supplier_func(session=session, suplier_name=supplier_name)
        price_data = []
        new_data = []
        print(f"all_data: {all_data[0:1] if all_data else 'No data'}")
        
        for item in all_data:
            print(f"item: {item}")
            # Перевіряємо, чи є в item ключ 'battery_id' (для словників)
            if isinstance(item, dict) and item['panel_id']:
                price_data.append({
                    "price": item['price'],
                    "panel_id": item['panel_id'],
                    "supplier_id": supplier_id
                })
            else:
                new_data.append(item)

        for item in price_data:
            await update_solar_panels_prices(session=session, solar_panel=item)

        print(f"new_data {len(new_data)} {new_data[0] if new_data else 'No data'}")

        if new_data:  # Перевіряємо, чи є нові дані
            prompt = add_new_prompt(new_data)
            result = await gemini_request(prompt)
            print(f"result: {result}")
            if result:  # Перевіряємо, чи є результат
                for item in result:
                    # Перевіряємо, чи item є словником
                    if isinstance(item, dict):
                        brand_name = item.get('brand')
                        brand_id = await get_or_create_brand(session=session, brand_name=brand_name)
                        solar_panel = SolarPanelCreateSchema(
                            full_name=item.get('full_name'),
                            power=item.get('power'),
                            region=item.get('region'),
                            panel_type=item.get('panel_type'),
                            cell_type=item.get('cell_type'),
                            thickness=item.get('thickness'),
                            panel_color=item.get('panel_color'),
                            frame_color=item.get('frame_color'),
                            brand_id=brand_id
                        )
                    else:  # Якщо item є об'єктом
                        brand_id = await get_or_create_brand(session=session, brand_name=item.brand)
                        solar_panel = SolarPanelCreateSchema(
                            full_name=item.full_name,
                            power=item.power,
                            region=item.region,
                            panel_type=item.panel_type,
                            cell_type=item.cell_type,
                            thickness=item.thickness,
                            panel_color=item.panel_color,
                            frame_color=item.frame_color,
                            brand_id=brand_id
                        )
                    
                    # Створюємо новий акумулятор
                    new_solar_panel = await create_solar_panel(session=session, solar_panel=solar_panel)
                    
                    # Додаємо ціну для нового акумулятора
                    if isinstance(item, dict):
                        price = item.get('price')
                    else:
                        price = getattr(item, 'price', 0)
                    
                    if new_solar_panel and price:
                        await update_solar_panels_prices(session=session, solar_panel={
                            "price": price,
                            "panel_id": new_solar_panel.id,
                            "supplier_id": supplier_id
                        })

    return "OK"