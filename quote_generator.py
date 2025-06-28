import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения (только для локального запуска)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Получение API-ключа OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

def generate_quote(user_message):
    if not OPENROUTER_API_KEY:
        # Заглушка, если API-ключ отсутствует
        return (
            f"Счастье — в простых вещах, что окружают нас.",
            f"Цени моменты радости, которые дарит жизнь."
        )
    
    # Инициализация клиента OpenAI для OpenRouter
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_API_URL
    )
    
    # Формируем запрос к DeepSeek API
    prompt = (
        f"Создай умное высказывание на русском языке по теме '{user_message}'. "
        "Формат ответа: основная цитата (1-2 предложения, максимум 100 символов) "
        "и дополнительное предложение (1-2 предложения, максимум 150 символов). "
        "Пример: 'Кто видит красоту в простом, никогда не остаётся без радости. "
        "Воспитывай благодарность и учись замечать маленькое счастье в повседневности.'"
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Ты — умный ассистент, создающий вдохновляющие цитаты."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        text = response.choices[0].message.content.strip()
        
        # Разделяем цитату и предложение
        lines = text.split("\n\n")
        if len(lines) >= 2:
            quote = lines[0][:100]  # Ограничиваем длину цитаты
            suggestion = lines[1][:150]  # Ограничиваем длину предложения
        else:
            quote = text[:100]
            suggestion = "Продолжай искать вдохновение в повседневности."
        
        return quote, suggestion
    except Exception as e:
        # Заглушка в случае ошибки API
        return (
            f"Счастье — в простых вещах, что окружают нас.",
            f"Цени моменты радости, которые дарит жизнь."
        )
        
        return quote, suggestion
    else:
        raise Exception(f"Ошибка API: {response.text}")
