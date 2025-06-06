from services.inverters.helpers.supplier import get_or_create_supplier
from services.inverters.helpers.me import get_or_create_me
from services.inverters.helpers.competitor import get_or_create_competitor
from services.inverters.helpers.inverters import update_inverters_prices
from services.inverters.helpers.brand import get_or_create_brand
from services.inverters.helpers.inverters import create_inverter
from services.inverters.backend.schemas import InverterCreateSchema
from prompts.inverters.get_prices_prompt import get_prices_prompt
from prompts.inverters.add_new_inverter_prompt import add_new_prompt
from filters.inverters_filter import ai_filter
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
            if isinstance(item, dict) and item['inverter_id']:
                price_data.append({
                    "price": item['price'],
                    "inverter_id": item['inverter_id'],
                    "supplier_id": supplier_id
                })
            else:
                new_data.append(item)

        for item in price_data:
            await update_inverters_prices(session=session, inverter=item)

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
                        inverter = InverterCreateSchema(
                            full_name=item.get('full_name'),
                            power=item.get('power'),
                            voltage=item.get('voltage'),
                            inverter_type=item.get('inverter_type'),
                            generation=item.get('generation'),
                            string_count=item.get('string_count'),
                            brand_id=brand_id
                        )
                    else:  # Якщо item є об'єктом
                        brand_id = await get_or_create_brand(session=session, brand_name=item.brand)
                        inverter = InverterCreateSchema(
                            full_name=item.full_name,
                            power=item.power,
                            voltage=item.voltage,
                            inverter_type=item.inverter_type,
                            generation=item.generation,
                            string_count=item.string_count,
                            brand_id=brand_id
                        )
                    
                    # Створюємо новий акумулятор
                    new_inverter = await create_inverter(session=session, inverter=inverter)
                    
                    # Додаємо ціну для нового акумулятора
                    if isinstance(item, dict):
                        price = item.get('price')
                    else:
                        price = getattr(item, 'price', 0)
                    
                    if new_inverter and price:
                        await update_inverters_prices(session=session, inverter={
                            "price": price,
                            "inverter_id": new_inverter.id,
                            "supplier_id": supplier_id
                        })

    return "OK"