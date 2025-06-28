import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import random

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения (только для локального запуска)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Получение API-ключа OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1"

def generate_quote(user_message):
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY не установлен, используется локальная цитата")
        return generate_local_quote(user_message)
    
    # Инициализация клиента OpenAI
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_URL
    )
    
    # Формируем запрос к OpenAI API
    prompt = (
        f"Создай умное высказывание на русском языке по теме '{user_message}'. "
        "Формат ответа: основная цитата (1-2 лаконичных предложения) и пояснение (1-2 лаконичных предложения). "
        "Раздели цитату и пояснение двумя переносами строки (\n\n). "
        "Пример:\n"
        "Жизнь — это путь, полный уроков и открытий.\n\n"
        "Каждый шаг учит нас ценить момент и расти."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Используем gpt-3.5-turbo для экономии
            messages=[
                {"role": "system", "content": "Ты — умный ассистент, создающий вдохновляющие цитаты на русском языке."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        text = response.choices[0].message.content.strip()
        logger.info(f"Ответ API: {text}")
        
        # Разделяем цитату и пояснение
        lines = text.split("\n\n")
        if len(lines) >= 2:
            quote = lines[0].strip()
            suggestion = lines[1].strip()
        else:
            # Резервный разбор, если API не вернул два блока
            sentences = text.replace("\n", " ").split(". ")
            if len(sentences) >= 2:
                quote = sentences[0].strip() + "."
                suggestion = ". ".join(sentences[1:]).strip() + "."
            else:
                quote = text.strip()
                suggestion = f"Размышляй над темой '{user_message}' и находи в ней вдохновение."
        
        logger.info(f"Сгенерировано: quote='{quote}', suggestion='{suggestion}'")
        return quote, suggestion
    except Exception as e:
        logger.error(f"Ошибка API: {str(e)}")
        return generate_local_quote(user_message)

def generate_local_quote(user_message):
    """Генерирует локальную цитату и пояснение на основе запроса."""
    user_message = user_message.lower().strip()
    
    # Словарь тем с цитатами и пояснениями
    quotes_db = {
        "жизнь": [
            ("Жизнь — это путешествие, а не пункт назначения.", "Цени каждый момент пути, он учит тебя новому."),
            ("Жизнь подобна книге, каждая страница — новый опыт.", "Пиши свою историю с вдохновением и смелостью.")
        ],
        "счастье": [
            ("Счастье — в умении находить радость в мелочах.", "Замечай красоту в каждом дне, и жизнь станет ярче."),
            ("Счастье — это выбор, который ты делаешь каждый день.", "Выбирай радость, даже в трудные моменты.")
        ],
        "успех": [
            ("Успех — это шаги вперёд, несмотря на преграды.", "Терпение и упорство приведут тебя к цели."),
            ("Успех начинается с веры в свои силы.", "Доверяй себе и действуй смело.")
        ]
    }
    
    # Поиск подходящей темы
    for theme in quotes_db:
        if theme in user_message:
            quote, suggestion = random.choice(quotes_db[theme])
            logger.info(f"Локальная цитата: quote='{quote}', suggestion='{suggestion}'")
            return quote, suggestion
    
    # Резервная цитата, если тема не найдена
    default_quote = f"{user_message.capitalize()} — это возможность расти и учиться."
    default_suggestion = f"Ищи вдохновение в '{user_message}', чтобы раскрыть свой потенциал."
    logger.info(f"Локальная цитата (резерв): quote='{default_quote}', suggestion='{default_suggestion}'")
    return default_quote, default_suggestion
