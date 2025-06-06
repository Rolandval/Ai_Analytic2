def parse_txt_prompt(text, comment):
    prompt = f"""
    Діяй як професійний парсер і спеціаліст з продажу інверторів для сонячних електростанцій.

!!! САМЕ ГОЛОВНЕ спочатку зрозумій чи є даний товар інвертором, і якщо ні то пропусти його

З цього TXT-фрагменту повністю витягни дані про інвертори та перетвори їх у масив JSON об'єктів такого формату:
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

📌 Деталі парсингу:
- 'brand': поверни назву бренду одним словом
- `price`: найменший оптовий (якщо неможливо знайти то null)
- `full_name`: повна назва інвертора 
- `power`: потужність в кВт (якщо немає то null)
- `inverter_type`: тип інвертора (gybrid/off-grid/on-grid)
- `generation`: покоління інвертора (за замовчуванням 4)
- `string_count`: кількість стрінгів (якщо немає то null)
- `firmware`: версія прошивки (якщо немає то null)
{comment if comment else ""}


Ось дані:
{text}

❗️Поверни лише чистий JSON у відповідь. Без зайвого тексту.
"""
    return prompt