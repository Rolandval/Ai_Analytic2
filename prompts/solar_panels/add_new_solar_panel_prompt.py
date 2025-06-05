def add_new_prompt(data):
    promt = f"""
    Дій як професійний спеціаліст з сонячних панелей.
    
    в мене є дані про сонячні панелі в форматі JSON
    {{
        "brand": brand,
        "power": power,
        "full_name": full_name,
        "price": price,
        "panel_type": panel_type,
        "cell_type": cell_type,
        "thickness": thickness
    }}
    де 
    - "brand": бренд
    - "power": потужність (Вт)
    - "full_name": повна назва
    - "price": ціна в доларах США
    - "panel_type": тип панелі (одностороння/двостороння)
    - "cell_type": тип комірок (n-type/p-type)
    - "thickness": товщина (мм)
    

    твоє завдання - проаналізувати дані про сонячні панелі які я тобі відправлю та дізнатись як мені записати правильно дану панель в мою базу даних
    але перш за все пропусти панель в якої хоча б одне поле є 0 або Null - їх видали
    всі які залишуться - то спробуй знайти в інтернеті правильні дані про модель і поверни мені JSON для запису її в такому форматі(не змінюй поле з ціною ніколи воно має залишитись таким як є!!!)
    {{
        "brand": brand,
        "power": power,
        "full_name": full_name,
        "price": price,
        "panel_type": panel_type,
        "cell_type": cell_type,
        "thickness": thickness
    }} 
    приклад:
    [
        {{
            "brand": "JinkoSolar",
            "power": 450.0,
            "full_name": "JinkoSolar Tiger Neo N-type 450W",
            "price": 150.0,
            "panel_type": "одностороння",
            "cell_type": "n-type",
            "thickness": 30.0
        }}
    ]

    поле full_name - повна назва сонячної панелі має бути повернено коректно без лишніх символів(знайди правильну назву в інтернеті)

    ❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
    якщо немає нічогго то поверни пустий список []


    дані:
    {data}
    """
    return promt