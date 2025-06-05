from services.solar_panels.helpers.solar_panels import get_all_solar_panels
import json

async def get_prices_prompt(data, session):
    solar_panels = await get_all_solar_panels(session=session)

    solar_panels_json = json.dumps(solar_panels, ensure_ascii=False, separators=(',', ':'))
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    prompt = f"""
Я маю дві групи даних:

1. Сонячні панелі з моєї бази даних:

2. Дані про сонячні панелі від постачальника:

Твоє завдання — для кожної сонячної панелі від постачальника знайти найбільш схожу сонячну панель з бази даних та повернути результат у вигляді списку об'єктів JSON.

Формат для кожного знайденого співпадіння:
{{
    "price": <float>,
    "panel_id": <int>
}}

Обов'язково має бути price!!!! без нього не повертай

Якщо не вдалося знайти схожу сонячну панель, поверни повний об'єкт постачальника з усіма полями, які він містить, але додай поле `"panel_id": null`. Наприклад:
{{
    "brand": "JinkoSolar", <str>
    "power": 450.0, <float>
    "full_name": "JinkoSolar Tiger Neo N-type 450W", <str>
    "price": 150.0, <float>
    "panel_type": "одностороння", <str>
    "cell_type": "n-type", <str>
    "thickness": 30.0, <float>
    "panel_id": null <null>
}}

Використовуй для порівняння такі поля: `brand`, `power`, `panel_type`, `cell_type`, `thickness`, `full_name`. Співпадіння повинно бути максимально точним(окрім поля full_name)

❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
1. Сонячні панелі з моєї бази даних:
{solar_panels_json}

2. Дані про сонячні панелі від постачальника:
{data_json}
    """
    return prompt
