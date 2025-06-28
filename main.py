import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
from quote_generator import generate_quote
from image_generator import create_quote_image

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения (только для локального запуска)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    logger.info(f"Загрузка файла .env из: {env_path}")
    load_dotenv(env_path)
else:
    logger.info("Файл .env не найден, используются переменные окружения из среды")

# Получение токена Telegram и URL webhook
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Проверка токена и URL
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не установлен")
    raise ValueError("TELEGRAM_TOKEN не установлен. Убедитесь, что он задан в .env или в переменных окружения.")
if not WEBHOOK_URL:
    logger.error("WEBHOOK_URL не установлен")
    raise ValueError("WEBHOOK_URL не установлен. Убедитесь, что он задан в .env или в переменных окружения.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    await update.message.reply_text(
        "Привет! Я бот, который создаёт умные высказывания. "
        "Напиши любой запрос, например, 'о счастье' или 'о жизни', "
        "и я сгенерирую цитату и изображение!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Получено сообщение: {user_message}")
    
    try:
        # Генерация цитаты через DeepSeek API
        quote, suggestion = generate_quote(user_message)
        
        # Создание изображения
        image_path = create_quote_image(quote, suggestion)
        
        # Отправка текста
        response = f"{quote}\n\n{suggestion}"
        await update.message.reply_text(response)
        
        # Отправка изображения
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
        
        # Удаление временного файла
        os.remove(image_path)
        
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка при генерации цитаты. Попробуйте снова!"
        )

def main():
    try:
        logger.info(f"Запуск бота с токеном: {TELEGRAM_TOKEN[:10]}...")
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запуск бота с webhook
        logger.info(f"Установка webhook: {WEBHOOK_URL}")
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 8443)),
            url_path="/webhook",
            webhook_url=WEBHOOK_URL
        )
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}")
        raise

if __name__ == "__main__":
    main()
