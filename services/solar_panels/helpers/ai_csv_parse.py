import csv
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


def ai_parser(csv_path: str, comment: str | None, chunk_size: int = 50):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Використовуємо доступну модель gemini-1.5-flash або gemini-pro
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.3,
            "top_p": 1,
            "top_k": 40,
            "max_output_tokens": 999999
        }
    )
    results = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    

        for i in range(0, len(rows), chunk_size):
            chunk = rows[i:i + chunk_size]

            # Формуємо CSV-рядок
            csv_chunk = [headers] + chunk
            csv_text = '\n'.join([','.join(row) for row in csv_chunk])

            prompt = f"""
Діяй як професійний парсер і спеціаліст з продажу сонячних панелей.

З цього CSV-фрагменту повністю витягни дані про сонячні панелі та перетвори їх у масив JSON об'єктів такого формату:
{{
  "brand": brand,
  "power": power,
  "full_name": full_name,
  "price": price,
  "panel_type": panel_type,
  "cell_type": cell_type,
  "thickness": thickness
}}

📌 Деталі парсингу:
- 'brand': поверни назву бренду одним словом
- `price`: ціна в доларах США, ціна завжди має бути (якщо немає то None) постарайся проаналізувати з рядка яке значення є найближчим
- `power`: потужність у Ватах (Вт/W), якщо не вказано ніяких букв то подумай логічно яке з цих значень найбільш наближене і реальне до потужності
- `panel_type`: тип панелі - "одностороння" або "двостороння" (за замовчуванням "одностороння")
- `cell_type`: тип комірок - "n-type" або "p-type" (за замовчуванням "n-type")
- `thickness`: товщина в міліметрах (мм) (за замовчуванням 30)
- `full_name`: повна назва сонячної панелі

{comment if comment else ""}

Ось CSV-дані:
{csv_text}

❗️Поверни лише чистий JSON у відповідь. Без зайвого тексту.
"""

            try:
                response = model.generate_content(prompt)
                response_text = response.text
                
                # Видаляємо зайві символи, які можуть заважати парсингу JSON
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text.replace("```json", "", 1)
                if response_text.endswith("```"):
                    response_text = response_text.rsplit("```", 1)[0]
                response_text = response_text.strip()
                
                # Парсимо JSON
                json_data = json.loads(response_text)
                results.extend(json_data)
                print(f"Успішно оброблено блок {i}-{i + len(chunk)}: знайдено {len(json_data)} сонячних панелей")
            except Exception as e:
                print(f"Помилка на блоці {i}-{i + chunk_size}: {e}")
                print(f"Відповідь API: {response.text if 'response' in locals() else 'Немає відповіді'}")
                continue

    return results
