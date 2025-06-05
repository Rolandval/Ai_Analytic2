import asyncio
import json
import time
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
import os

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
    text = data["batteries"]
    prompt = f"""
Діяй як професійний парсер і спеціаліст з продажу автомобільних акумуляторів.

З цього HTML-фрагменту повністю витягни дані про акумулятори та перетвори їх у масив JSON об'єктів такого формату:
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

📌 Деталі парсингу:
- 'brand': поверни назву бренду одним словом
- `price`: найменший оптовий (якщо неможкш знайти то 0
- `full_name`: повна назва батареї
- `c_amps`: пусковий струм(якщо немає то 0)
- `region`: за замовчуванням EUROPE, якщо є "ASIA", то ASIA (це є тип корпусу)
- `polarity`: у форматі R+ або L+ (в залежності з якої сторони +(якщо пише (-/+) то це R+)))
- `electrolyte`: AGM, GEL, або LAB (якщо не вказаний)
- `volume`: ємність в Ah (в деяких випадках ємність може позначатись на укр/рос мові типу АГ, АЧ, Аг, Ач, аг, ач)

Ось HTML-дані:
{text}

❗️Поверни лише чистий JSON у відповідь. Без зайвого тексту.
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
        print(f"✅ Оброблено блок {index}: знайдено {len(parsed)} акумуляторів")
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




