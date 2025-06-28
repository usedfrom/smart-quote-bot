import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from quote_generator import generate_quote
from image_generator import create_image

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот, создающий вдохновляющие цитаты. "
        "Напиши тему (например, 'жизнь', 'счастье', 'успех', 'любовь', 'вдохновение'), "
        "и я создам цитату с пояснением!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    theme = update.message.text.strip()
    await asyncio.sleep(1)  # Задержка для предотвращения лимитов API
    try:
        quote, suggestion = await generate_quote(theme)  # Добавлен await
        image_path = create_image(quote, suggestion)
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"{quote}\n\n{suggestion}"
            )
        os.remove(image_path)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    print(f"Запуск бота с токеном: {token[:10]}...")
    app = Application.builder().token(token).build()
    print("Бот запускается в режиме polling...")
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
