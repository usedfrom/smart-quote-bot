import os
import random
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = "http://iqmwofty:jk8uespriwzc@45.127.248.127:5128"

quotes_db = {
    "жизнь": [
        {"quote": "Жизнь — это полотно, которое ты рисуешь каждый день.", "suggestion": "Выбирай яркие краски для своих моментов."},
        {"quote": "Жизнь подобна книге, где каждая страница — новый шанс.", "suggestion": "Пиши свою историю с вдохновением и смелостью."},
        {"quote": "Жизнь — это путешествие, а не пункт назначения.", "suggestion": "Цени каждый шаг, даже если путь извилист."}
    ],
    "счастье": [
        {"quote": "Счастье — это момент, когда ты ценишь то, что есть.", "suggestion": "Найди радость в простых вещах вокруг."},
        {"quote": "Счастье рождается в сердце, а не в обстоятельствах.", "suggestion": "Ищи внутренний покой, чтобы сиять снаружи."},
        {"quote": "Счастье — это делиться радостью с другими.", "suggestion": "Улыбка другу умножает твою собственную радость."}
    ],
    "успех": [
        {"quote": "Успех — это движение вперёд, несмотря на преграды.", "suggestion": "Каждый маленький шаг приближает к большой цели."},
        {"quote": "Успех приходит к тем, кто действует, а не ждёт.", "suggestion": "Начни сегодня, и завтра будешь ближе к мечте."},
        {"quote": "Успех — это умение учиться на ошибках.", "suggestion": "Каждая неудача — урок для будущего триумфа."}
    ],
    "любовь": [
        {"quote": "Любовь — это свет, который согревает даже в темноте.", "suggestion": "Дари любовь, и она вернётся к тебе вдвойне."},
        {"quote": "Любовь — это когда два сердца бьются в унисон.", "suggestion": "Слушай своё сердце и уважай ритм другого."},
        {"quote": "Любовь — это свобода быть собой рядом с другим.", "suggestion": "Цени тех, кто принимает тебя без масок."}
    ],
    "вдохновение": [
        {"quote": "Вдохновение — это искра, зажигающая твои мечты.", "suggestion": "Ищи её в природе, людях и своих мыслях."},
        {"quote": "Вдохновение приходит, когда ты открыт новому.", "suggestion": "Экспериментируй и не бойся пробовать."},
        {"quote": "Вдохновение — это ветер, дующий в паруса идей.", "suggestion": "Лови его и направляй к своим целям."}
    ]
}

async def generate_quote(theme: str) -> tuple[str, str]:
    if theme.lower() not in quotes_db:
        theme = random.choice(list(quotes_db.keys()))
    
    try:
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            http_client=httpx.AsyncClient(
                proxies=PROXY_URL,
                timeout=30.0
            )
        )
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — философ, создающий лаконичные цитаты (1-2 предложения) и пояснения (1-2 предложения), разделённые \\n\\n. Отвечай только в этом формате."},
                {"role": "user", "content": f"Создай цитату о теме '{theme}' в формате: цитата (1-2 предложения)\\n\\nПояснение (1-2 предложения)"}
            ],
            max_tokens=400,
            temperature=0.7
        )
        content = response.choices[0].message.content
        print(f"Ответ API: {content}")
        quote, suggestion = content.split("\n\n", 1)
        return quote.strip(), suggestion.strip()
    except Exception as e:
        print(f"Ошибка API: {str(e)}")
        if "insufficient_quota" in str(e).lower():
            quote_data = random.choice(quotes_db[theme.lower()])
            print(f"Локальная цитата: quote='{quote_data['quote']}', suggestion='{quote_data['suggestion']}'")
            return quote_data["quote"], quote_data["suggestion"]
        else:
            raise e
