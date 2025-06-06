from services.inverters.helpers.inverters import get_all_inverters
import json

async def get_prices_prompt(data, session):
    inverters = await get_all_inverters(session=session)

    inverters_json = json.dumps(inverters, ensure_ascii=False, separators=(',', ':'))
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    prompt = f"""
Я маю дві групи даних:

1. Інвертори з моєї бази даних:

2. Дані про інвертори від постачальника:

Твоє завдання — для кожного інвертора від постачальника знайти найбільш схожий інвертор з бази даних та повернути результат у вигляді списку об'єктів JSON.

Формат для кожного знайденого співпадіння:
{{
    "price": <float>,
    "inverter_id": <int>
}}

Обов'язково має бути price!!!! без нього не повертай

Якщо не вдалося знайти схожий інвертор, поверни повний об'єкт постачальника з усіма полями, які він містить, але додай поле `"inverter_id": null`. Наприклад:
{{
    "brand": "Huawei", <str>
    "power": 10.0, <float>
    "full_name": "Huawei SUN2000-10KTL-M1", <str>
    "price": 2500.0, <float>
    "inverter_type": "on-grid", <str>
    "generation": 3, <int>
    "string_count": 2, <int>
    "firmware": "V300R001", <str>
    "inverter_id": null <null>
}}

Використовуй для порівняння такі поля: `brand`, `power`, `inverter_type`, `generation`, `string_count`, `full_name`. Співпадіння повинно бути максимально точним(окрім поля full_name)

❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
1. Інвертори з моєї бази даних:
{inverters_json}

2. Дані про інвертори від постачальника:
{data_json}
    """
    return prompt
