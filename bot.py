import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from db import load_subscribers, save_subscriber
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_subscriber(chat_id)
    await update.message.reply_text("Вы подписаны на уведомления.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    start_scheduler(application)
    logging.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
