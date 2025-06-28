import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import random
import time
import openai
import httpx

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

# Настройка прокси
PROXY_ADDRESS = "104.239.105.125"
PROXY_PORT = 6655
PROXY_USERNAME = "iqmwofty"
PROXY_PASSWORD = "jk8uespriwzc"
PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_ADDRESS}:{PROXY_PORT}"

def generate_quote(user_message):
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY не установлен, используется локальная цитата")
        return generate_local_quote(user_message)
    
    # Инициализация HTTP-клиента с прокси
    http_client = httpx.Client(
        proxies={
            "http://": PROXY_URL,
            "https://": PROXY_URL,
        },
        timeout=30.0
    )
    
    # Инициализация клиента OpenAI с прокси
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_URL,
        http_client=http_client
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
    
    max_retries = 5  # Количество попыток для временных ошибок
    retry_delay = 2  # Начальная задержка в секундах
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
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
            http_client.close()  # Закрываем HTTP-клиент
            return quote, suggestion
        
        except openai.RateLimitError as e:
            if "insufficient_quota" in str(e).lower():
                logger.error(f"Ошибка API: Исчерпана квота - {str(e)}")
                http_client.close()
                return generate_local_quote(user_message)
            if attempt < max_retries - 1:
                logger.warning(f"Ошибка 429, повторная попытка {attempt + 1}/{max_retries} через {retry_delay} сек.")
                time.sleep(retry_delay)
                retry_delay *= 2  # Экспоненциальная задержка
            else:
                logger.error(f"Ошибка API: {str(e)}")
                http_client.close()
                return generate_local_quote(user_message)
        except Exception as e:
            logger.error(f"Ошибка API: {str(e)}")
            http_client.close()
            return generate_local_quote(user_message)

def generate_local_quote(user_message):
    """Генерирует локальную цитату и пояснение на основе запроса."""
    user_message = user_message.lower().strip()
    
    # Расширенная база локальных цитат
    quotes_db = {
        "жизнь": [
            ("Жизнь — это путешествие, а не пункт назначения.", "Цени каждый момент пути, он учит тебя новому."),
            ("Жизнь подобна книге, каждая страница — новый опыт.", "Пиши свою историю с вдохновением и смелостью."),
            ("Жизнь — это танец под мелодию времени.", "Слушай ритм каждого дня и двигайся в гармонии."),
            ("Жизнь — это полотно, которое ты рисуешь каждый день.", "Выбирай яркие краски для своих моментов."),
            ("Жизнь — это загадка, раскрываемая с каждым шагом.", "Ищи ответы в простых радостях и уроках.")
        ],
        "счастье": [
            ("Счастье — в умении находить радость в мелочах.", "Замечай красоту в каждом дне, и жизнь станет ярче."),
            ("Счастье — это выбор, который ты делаешь каждый день.", "Выбирай радость, даже в трудные моменты."),
            ("Счастье — это тепло в сердце от простых мгновений.", "Делись добротой, и счастье вернётся к тебе."),
            ("Счастье — это момент, когда душа поёт.", "Найди гармонию в себе, чтобы почувствовать его."),
            ("Счастье — это свет, который ты создаёшь внутри.", "Разожги его, и оно осветит твой путь.")
        ],
        "успех": [
            ("Успех — это шаги вперёд, несмотря на преграды.", "Терпение и упорство приведут тебя к цели."),
            ("Успех начинается с веры в свои силы.", "Доверяй себе и действуй смело."),
            ("Успех — это плод настойчивости и мечты.", "Ставь цели и иди к ним с решимостью."),
            ("Успех — это момент, когда труд встречается с возможностью.", "Будь готов к своему шансу."),
            ("Успех — это путь через ошибки к победам.", "Каждая неудача — шаг к триумфу.")
        ],
        "любовь": [
            ("Любовь — это свет, который согревает душу.", "Дари любовь, и она умножится в твоей жизни."),
            ("Любовь — это искусство видеть сердце другого.", "Будь открытым, и любовь найдёт тебя."),
            ("Любовь — это мост между двумя душами.", "Строй его с заботой и доверием."),
            ("Любовь — это сила, дарящая крылья.", "Позволь ей вдохновлять тебя на лучшее.")
        ],
        "вдохновение": [
            ("Вдохновение — это искра, зажигающая мечты.", "Ищи её в каждом дне и твори с душой."),
            ("Вдохновение рождается в тишине сердца.", "Слушай себя, и идеи придут сами."),
            ("Вдохновение — это дыхание новых идей.", "Откройся миру, чтобы поймать его поток."),
            ("Вдохновение — это ключ к твоему потенциалу.", "Найди его в простых вещах вокруг.")
        ]
    }
    
    # Поиск подходящей темы
    for theme in quotes_db:
        if theme in user_message:
            quote, suggestion = random.choice(quotes_db[theme])
            logger.info(f"Локальная цитата: quote='{quote}', suggestion='{suggestion}'")
            return quote, suggestion
    
    # Резервная цитата для неизвестных тем
    default_quote = f"В '{user_message}' кроется уникальная возможность для роста."
    default_suggestion = f"Найди смысл в '{user_message}', чтобы открыть новые горизонты."
    logger.info(f"Локальная цитата (резерв): quote='{default_quote}', suggestion='{default_suggestion}'")
    return default_quote, default_suggestion
