from services.batteries.helpers.supplier import get_or_create_supplier
from services.batteries.helpers.me import get_or_create_me
from services.batteries.helpers.competitor import get_or_create_competitor
from services.batteries.helpers.batteries import update_batteries_prices
from services.batteries.helpers.brand import get_or_create_brand
from services.batteries.helpers.batteries import create_battery
from services.batteries.backend.schemas import BatteryCreateSchema
from prompts.batteries.get_prices_prompt import get_prices_prompt
from prompts.batteries.add_new_battery_prompt import add_new_prompt
from filters.batteries_filter import ai_filter
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
            if isinstance(item, dict) and item['battery_id']:
                price_data.append({
                    "price": item['price'],
                    "battery_id": item['battery_id'],
                    "supplier_id": supplier_id
                })
            else:
                new_data.append(item)

        for item in price_data:
            await update_batteries_prices(session=session, battery=item)

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
                        battery = BatteryCreateSchema(
                            full_name=item.get('full_name'),
                            c_amps=item.get('c_amps'),
                            volume=item.get('volume'),  # Додаємо поле volume
                            region=item.get('region'),
                            polarity=item.get('polarity'),
                            electrolyte=item.get('electrolyte'),
                            brand_id=brand_id
                        )
                    else:  # Якщо item є об'єктом
                        brand_id = await get_or_create_brand(session=session, brand_name=item.brand)
                        battery = BatteryCreateSchema(
                            full_name=item.full_name,
                            c_amps=item.c_amps,
                            volume=getattr(item, 'volume', None),  # Безпечно отримуємо volume
                            region=item.region,
                            polarity=item.polarity,
                            electrolyte=item.electrolyte,
                            brand_id=brand_id
                        )
                    
                    # Створюємо новий акумулятор
                    new_battery = await create_battery(session=session, battery=battery)
                    
                    # Додаємо ціну для нового акумулятора
                    if isinstance(item, dict):
                        price = item.get('price')
                    else:
                        price = getattr(item, 'price', 0)
                    
                    if new_battery and price:
                        await update_batteries_prices(session=session, battery={
                            "price": price,
                            "battery_id": new_battery.id,
                            "supplier_id": supplier_id
                        })

    return "OK"