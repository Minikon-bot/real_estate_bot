import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN or TOKEN.startswith("ВАШ_ТОКЕН"):
    raise ValueError("Переменная TELEGRAM_BOT_TOKEN не установлена или некорректна!")

# Список подписчиков
subscribers = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляем пользователя в подписчики"""
    user_id = update.effective_chat.id
    subscribers.add(user_id)
    await update.message.reply_text("Вы подписаны на уведомления!")

async def notify_all(message: str, application):
    """Отправка уведомления всем подписчикам"""
    for user_id in subscribers:
        try:
            await application.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение {user_id}: {e}")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logging.info("Бот запущен...")
    application.run_polling()
