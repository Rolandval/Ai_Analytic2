import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


async def analytics_prompt(prompt):
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
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        return response_text
    except Exception as e:
        print(f"Помилка аналізу: {e}")
        return "Помилка аналізу"