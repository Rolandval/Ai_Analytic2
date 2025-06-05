

def add_new_prompt(data):
    promt = f"""
    Дій як професійний спеціаліст з автомобільних акумуляторів.
    
    в мене є дані про акумулятори в форматі JSON
    {{
        "brand": brand,
        "volume": volume,
        "full_name": full_name,
        "price": price,
        "c_amps": c_amps,
        "region": region,
        "polarity": polarity,
        "electrolyte": electrolyte
    }}
    де 
    - "brand": бренд
    - "volume": обʼєм
    - "full_name": повна назва
    - "price": ціна
    - "c_amps": пусковий струм
    - "region": тип корпусу (EUROPE, ASIA)
    - "polarity": полярність (R+ або R-)
    - "electrolyte": тип електроліту (LAB, AGM, GEL)
    

    твоє завдання - проаналізувати дані прпо акумулятори які я тобі відправлю та дізнатись як мені записати правильно даний акумулятор в мою базу даних
    але перш за все пропусти акумулятор в якого хоча б одне поле є 0 або Null - їх видали
    всі які залишуться - то спробуй знайти в інтернеті правильні дані про модель і поаерни менні JSON для запису її в такому форматі(не змінюй поле з ціною ніколи воно має залишитись таким як є!!!)
    {{
        "brand": brand,
        "volume": volume,
        "full_name": full_name,
        "price": price,
        "c_amps": c_amps,
        "region": region,
        "polarity": polarity,
        "electrolyte": electrolyte
    }} 
    приклад:
    [
        {{
            "brand": "Varta",
            "volume": 60.0,
            "full_name": "Varta Blue Dynamic D24",
            "price": 1250.0,
            "c_amps": 540,
            "region": "EUROPE",
            "polarity": "R+",
            "electrolyte": "LAB"
        }}
    ]

    поле full_name - повна назва акумулятора має бути повернено коректно без лишніх символів(знайди правильну назву в інтернеті)

    ❗️Поверни лише **чистий JSON без пояснень**, без додаткового тексту.
    якщо немає нічогго то поверни пустий список []


    дані:
    {data}
    """
    return promt