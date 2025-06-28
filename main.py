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

# Загрузка переменных окружения
env_path = os.path.join(os.path.dirname(__file__), '.env')
logger.info(f"Попытка загрузки файла .env из: {env_path}")
if not os.path.exists(env_path):
    logger.error(f"Файл .env не найден по пути: {env_path}")
    raise FileNotFoundError(f"Файл .env не найден по пути: {env_path}")

load_dotenv(env_path)
logger.info(f"Содержимое .env загружено: TELEGRAM_TOKEN={os.getenv('TELEGRAM_TOKEN')[:10]}...")

# Получение токена Telegram из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверка токена
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не найден в файле .env")
    raise ValueError("TELEGRAM_TOKEN не установлен. Убедитесь, что файл .env содержит корректный токен.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    await update.message.reply_text(
        "Привет! Я бот, который создаёт умные высказывания. "
        "Напиши, например: 'Создай умное высказывание о счастье', "
        "и я сгенерирую цитату и изображение!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Получено сообщение: {user_message}")
    
    if "создай" in user_message.lower() or "цитата" in user_message.lower():
        try:
            # Генерация цитаты через Grok API
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
    else:
        await update.message.reply_text(
            "Напишите запрос, например: 'Создай умное высказывание о счастье'"
        )

def main():
    try:
        logger.info(f"Запуск бота с токеном: {TELEGRAM_TOKEN[:10]}...")  # Вывод первых 10 символов токена для проверки
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запуск бота
        logger.info("Бот запускается...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}")
        raise

if __name__ == "__main__":
    main()