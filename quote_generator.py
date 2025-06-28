import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения (только для локального запуска)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Получение API-ключа OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

def generate_quote(user_message):
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY не установлен, используется заглушка")
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
        "Формат ответа: основная цитата (1-2 предложения, до 100 символов) "
        "и дополнительное предложение (1-2 предложения, до 150 символов). "
        "Раздели цитату и предложение двумя переносами строки (\n\n). "
        "Пример:\n"
        "Кто видит красоту в простом, никогда не остаётся без радости.\n\n"
        "Воспитывай благодарность и учись замечать маленькое счастье в повседневности."
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Ты — умный ассистент, создающий вдохновляющие цитаты на русском языке."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Увеличено для более длинных ответов
            temperature=0.7
        )
        
        text = response.choices[0].message.content.strip()
        logger.info(f"Ответ API: {text}")
        
        # Разделяем цитату и предложение
        lines = text.split("\n\n")
        if len(lines) >= 2:
            quote = lines[0][:100].strip()  # Ограничиваем длину цитаты
            suggestion = lines[1][:150].strip()  # Ограничиваем длину предложения
        else:
            # Резервный разбор, если API не вернул два блока
            sentences = text.replace("\n", " ").split(". ")
            if len(sentences) >= 2:
                quote = sentences[0][:100].strip() + "."
                suggestion = ". ".join(sentences[1:])[:150].strip() + "."
            else:
                quote = text[:100].strip()
                suggestion = "Продолжай искать вдохновение в повседневности."
        
        logger.info(f"Сгенерировано: quote='{quote}', suggestion='{suggestion}'")
        return quote, suggestion
    except Exception as e:
        logger.error(f"Ошибка API: {str(e)}")
        return (
            f"Счастье — в простых вещах, что окружают нас.",
            f"Цени моменты радости, которые дарит жизнь."
        )
