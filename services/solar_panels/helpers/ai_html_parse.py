import asyncio
import json
import time
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
import os

from helpers.get_currency_rate import get_currency_rate

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 40,
        "max_output_tokens": 999999
    }
)


def parse_chunk(index: int, data: Dict[str, str]) -> List[Dict]:
    text = data["solar_panels"]
    prompt = f"""
Діяй як професійний парсер і спеціаліст з продажу сонячних панелей.

курс долара: {get_currency_rate()}

З цього HTML-фрагменту повністю витягни дані про сонячні панелі та перетвори їх у масив JSON об'єктів такого формату:
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
- 'brand': поверни назву бренду одним або двома словами
- `price`: ціна в доларах США (якщо ціна вказана в гривнях або є аідозріло велтикою(більше 2000) то перетвори її в долар)
- `full_name`: повна назва сонячної панелі
- `power`: потужність у Ватах (Вт/W) (якщо немає то None)
- `panel_type`: тип панелі - "одностороння" або "двостороння" (за замовчуванням None)
- `cell_type`: тип комірок - "n-type" або "p-type" (за замовчуванням None)
- `thickness`: товщина в міліметрах (мм) (за замовчуванням None)
- `panel_color`: колір панелі - "Default" або "All_Black" (за замовчуванням Default)
- `frame_color`: колір рамки - "silver" або "black" (за замовчуванням None)
- `price_per_w`: ціна за Вт/W (якщо price None то price_per_w None)

Ось HTML-дані:
{text}

❗️Поверни лише чистий JSONу такому форматі якому я просив у відповідь. Без зайвого тексту.
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Очищення
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
        if response_text.endswith("```"):
            response_text = response_text.rsplit("```", 1)[0]

        parsed = json.loads(response_text)
        print(f"✅ Оброблено блок {index}: знайдено {len(parsed)} сонячних панелей")
        return parsed

    except Exception as e:
        print(f"❌ Помилка на блоці {index}: {e}")
        return []


async def ai_parser(all_data: List[Dict[str, str]]) -> List[Dict]:
    parsed_results = []
    min_request_time = 10
    for i, data in enumerate(all_data):
        start_time = time.time()
        result = parse_chunk(i, data)
        parsed_results.extend(result)

        elapsed_time = time.time() - start_time
        if elapsed_time < min_request_time and i < len(all_data) - 1:  # не чекаємо після останнього запиту
            wait_time = min_request_time - elapsed_time
            print(f"⏳ Запит виконано за {elapsed_time:.1f} сек. Очікування {wait_time:.1f} секунд перед наступним запитом...")
            time.sleep(wait_time)


    return parsed_results




