import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения (только для локального запуска)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Получение API-ключа xAI
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

def generate_quote(user_message):
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY не установлен. Убедитесь, что он задан в .env или в переменных окружения.")
    
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Формируем запрос к Grok API
    prompt = (
        f"Создай умное высказывание на русском языке по теме '{user_message}'. "
        "Формат ответа: основная цитата (1-2 предложения, максимум 100 символов) "
        "и дополнительное предложение (1-2 предложения, максимум 150 символов). "
        "Пример: 'Кто видит красоту в простом, никогда не остаётся без радости. "
        "Воспитывай благодарность и учись замечать маленькое счастье в повседневности.'"
    )
    
    payload = {
        "model": "grok",
        "messages": [
            {"role": "system", "content": "Ты — умный ассистент, создающий вдохновляющие цитаты."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    
    response = requests.post(XAI_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Разделяем цитату и предложение
        lines = text.strip().split("\n\n")
        if len(lines) >= 2:
            quote = lines[0]
            suggestion = lines[1]
        else:
            quote = text[:100]
            suggestion = "Продолжай искать вдохновение в повседневности."
        
        return quote, suggestion
    else:
        raise Exception(f"Ошибка API: {response.text}")
