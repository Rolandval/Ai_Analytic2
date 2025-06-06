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


def parse_chunk(index, data) -> List[Dict]:
    prompt = f"""
Твоя роль — досвідчений спеціаліст з парсингу та продажу інверторів для сонячних електростанцій.

🔧 Я надаю тобі список даних у форматі JSON:
Кожен об'єкт містить поля:
- "brand": бренд
- "power": потужність (кВт)
- "full_name": повна назва
- "price": ціна в доларах США
- "inverter_type": тип інвертора (gybrid/off-grid/on-grid)
- "generation": покоління інвертора(1-5)
- "string_count": кількість стрінгів
- "firmware": версія прошивки (може бути відсутня)

🎯 Завдання:
якщо поля full_name немає то пропусти цей інвертор і не повертай його!
твоя задача проаналізувати наскільки реальні дані які тобі прийшли.
- якщо ти бачиш що ціна є більш ніж на 250% від середньої то пропусти цей інвертор, також якщо ціна є None або 0 то пропусти цей інвертор
- якщо ти бачиш що потужність є занадто великою (більше 100 кВт) або занадто малою (менше 1 кВт) то пропусти цей інвертор
- якщо ти бачиш що кількість стрінгів є занадто великою (більше 12) то пропусти цей інвертор
Проаналізуй поле `full_name`, і якщо:
- можеш визначити потужність з назви, якщо вона відсутня або некоректна
- можеш визначити тип інвертора з назви (гібридний/мережевий/автономний)
- інші параметри можеш також проаналізувати та виправити але вони в 97% випадків правильні

❗️У відповідь поверни **ті самі об'єкти JSON**, просто відфільтровані

📌 Важливо:
- ❗️Поверни лише чистий JSON у відповідь. Без зайвого тексту. 
- Якщо нічого не треба змінювати — просто поверни ті самі об'єкти без змін.
- дані мають повернутися в ті самому форматі як і прийшли просто відфільтровані(якщо це необхідно)
- дані поверни в форматі - 
- "brand": brand
- "power": power(float)
- "full_name": full_name
- "price": price(float)
- "inverter_type": inverter_type
- "generation": generation(int)
- "string_count": string_count(int)
- "firmware": firmware

також якщо бачиш що якись з параметрів не передався, то пропускай цей інвертор


Ось дані:
{data}
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
        return parsed

    except Exception as e:
        return []


def ai_filter(data: list):
    parsed_results = []
    min_request_time = 10
    total_items = len(data)
    
    print(f"Початок фільтрації {total_items} товарів")
    
    # Визначаємо розмір частини (chunk)
    chunk_size = 50
    
    # Розбиваємо список на частини
    for i in range(0, total_items, chunk_size):
        # Беремо частину даних (не більше chunk_size елементів)
        chunk = data[i:i + chunk_size]
        chunk_count = len(chunk)
        
        print(f"Обробка частини {i//chunk_size + 1}: {chunk_count} елементів")
        
        if chunk_count == 0:
            continue  # Пропускаємо порожні частини
        
        start_time = time.time()
        
        # Відправляємо частину на обробку
        chunk_index = i // chunk_size
        print(f"chunk: {len(chunk)}")
        result = parse_chunk(chunk_index, chunk)
        print(f"result: {len(result)}")

        
        if result:
            for item in result:
                parsed_results.append(item)
            
        elapsed_time = time.time() - start_time
        
        # Додаємо затримку між обробкою частин, якщо це не остання частина
        if i + chunk_size < total_items:
            if elapsed_time < min_request_time:
                wait_time = min_request_time - elapsed_time
                print(f"⏳ Частину оброблено за {elapsed_time:.1f} сек. Очікування {wait_time:.1f} секунд перед наступною частиною...")
                time.sleep(wait_time)
    
    print(f"✅ Фільтрацію завершено. Знайдено {len(parsed_results)} товарів")
    return parsed_results