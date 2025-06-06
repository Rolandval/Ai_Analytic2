from helpers.get_currency_rate import get_currency_rate


def parse_txt_prompt(text, comment):
    currency_rate = get_currency_rate()
    prompt = f"""
    Діяй як професійний парсер і спеціаліст з продажу сонячних панелей.

!!! САМЕ ГОЛОВНЕ спочатку зрозумій чи є даний товар сонячною панеллю, і якщо ні то пропусти його

курс долара: {currency_rate} - якщо потрібно

перш за все проаналізуй в якій валюті записана ціна якщо це можливо

З цього TXT-фрагменту повністю витягни дані про сонячні панелі та перетвори їх у масив JSON об'єктів такого формату:
{{
  "brand": brand,
  "power": power,
  "full_name": full_name,
  "price": price,
  "panel_type": panel_type,
  "cell_type": cell_type,
  "thickness": thickness,
  "panel_color": panel_color,
  "frame_color": frame_color,
  "price_per_w": price_per_w
}}

📌 Деталі парсингу:
- 'brand': поверни назву бренду одним словом
- `price`: ціна в доларах США (якщо бачиш що ціна більша як 2000 то скоріш за все ціна вказана в гривнях, тоді переведи)
- `full_name`: повна назва сонячної панелі
- `power`: потужність у Ватах (Вт/W)
- `panel_type`: тип панелі - "одностороння" або "двостороння" (якщо немає то None)
- `cell_type`: тип комірок - "n-type" або "p-type" (якщо немає то None)
- `thickness`: товщина в міліметрах (мм) (якщо немає то None)
- `panel_color`: колір панелі - "Default" або "All_Black" (якщо немає то None)
- `frame_color`: колір рамки - "silver" або "black" (якщо немає то None)
- `price_per_w`: ціна за Вт/W (якщо немає то None)

{comment if comment else ""}


Ось дані:
{text}

❗️Поверни лише чистий JSON у відповідь. Без зайвого тексту.
"""
    return prompt