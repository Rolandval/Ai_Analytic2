from services.batteries.helpers.batteries import get_all_batteries
import json

async def get_prices_prompt(data, session):
    batteries = await get_all_batteries(session=session)

    batteries_json = json.dumps(batteries, ensure_ascii=False, separators=(',', ':'))
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    prompt = f"""
Я маю дві групи даних:

1. Акумулятори з моєї бази даних:

2. Дані про акумулятори від постачальника:

Твоє завдання — для кожного акумулятора від постачальника знайти найбільш схожий акумулятор з бази даних та повернути результат у вигляді списку об'єктів JSON.

Формат для кожного знайденого співпадіння:
{{
    "price": <float>,
    "battery_id": <int>
}}

Обов'язково має бути price!!!! без нього не повертай

Якщо не вдалося знайти схожий акумулятор, поверни повний об'єкт постачальника з усіма полями, які він містить, але додай поле `"battery_id": null`. Наприклад:
{{
    "brand": "Varta", <str>
    "volume": 60.0, <float>
    "full_name": "Varta Blue Dynamic D24", <str>
    "price": 1250.0, <float>
    "c_amps": 540, <int>
    "region": "EUROPE", <str>
    "polarity": "R+", <str>
    "electrolyte": "LAB", <str>
    "battery_id": null <null>
}}

Використовуй для порівняння такі поля: `brand`, `volume`, `c_amps`, `polarity`, `electrolyte`, `region`, `full_name`. Співпадіння повинно бути максимально точним(окрім поля full_name)

❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
1. Акумулятори з моєї бази даних:
{batteries_json}

2. Дані про акумулятори від постачальника:
{data_json}
    """
    return prompt
