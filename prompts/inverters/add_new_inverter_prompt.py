def add_new_prompt(data):
    promt = f"""
    Дій як професійний спеціаліст з інверторів для сонячних електростанцій.
    
    в мене є дані про інвертори в форматі JSON
    {{
        "brand": brand,
        "power": power,
        "full_name": full_name,
        "price": price,
        "inverter_type": inverter_type,
        "generation": generation,
        "string_count": string_count,
        "firmware": firmware
    }}
    де 
    - "brand": бренд
    - "power": потужність (кВт)
    - "full_name": повна назва
    - "price": ціна в доларах США
    - "inverter_type": тип інвертора (gybrid/off-grid/on-grid)
    - "generation": покоління інвертора
    - "string_count": кількість стрінгів
    - "firmware": версія прошивки (може бути відсутня)
    

    твоє завдання - проаналізувати дані про інвертори які я тобі відправлю та дізнатись як мені записати правильно даний інвертор в мою базу даних
    але перш за все пропусти інвертор в якого хоча б одне поле є 0 або Null (крім firmware, яке може бути Null) - їх видали
    всі які залишуться - то спробуй знайти в інтернеті правильні дані про модель і поверни мені JSON для запису її в такому форматі(не змінюй поле з ціною ніколи воно має залишитись таким як є!!!)
    {{
        "brand": brand,
        "power": power,
        "full_name": full_name,
        "price": price,
        "inverter_type": inverter_type,
        "generation": generation,
        "string_count": string_count,
        "firmware": firmware
    }} 
    приклад:
    [
        {{
            "brand": "Huawei",
            "power": 10.0,
            "full_name": "Huawei SUN2000-10KTL-M1",
            "price": 2500.0,
            "inverter_type": "on-grid",
            "generation": 3,
            "string_count": 2,
            "firmware": "V300R001"
        }}
    ]

    поле full_name - повна назва інвертора має бути повернено коректно без лишніх символів(знайди правильну назву в інтернеті)

    ❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
    якщо немає нічогго то поверни пустий список []


    дані:
    {data}
    """
    return promt